import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HOME_URL = "https://tutorials.wufeng.de/lebara/"


def normalize_href(href):
    value = unquote(str(href).strip())
    parsed = urlparse(value)
    path = parsed.path if parsed.scheme or parsed.netloc else value.split("?", 1)[0]
    path = path.lstrip("./")
    if path.startswith("lebara/"):
        path = path[len("lebara/") :]
    return path


def load_article_order(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"order"}:
        raise ValueError("article-order.json 必须只包含 order 数组")

    order = data["order"]
    if not isinstance(order, list):
        raise ValueError("article-order.json 的 order 必须是数组")
    if any(type(issue_number) is not int or issue_number <= 0 for issue_number in order):
        raise ValueError("order 只能包含大于 0 的 Issue 整数编号")
    if len(order) != len(set(order)):
        raise ValueError("order 中不能有重复的 Issue 编号")
    return order


def build_rank_by_url(order, blog_base):
    posts = blog_base.get("postListJson")
    if not isinstance(posts, dict):
        raise ValueError("blogBase.json 缺少 postListJson")

    rank_by_url = {}
    missing = []
    for rank, issue_number in enumerate(order):
        post = posts.get(f"P{issue_number}")
        if not isinstance(post, dict) or not post.get("postUrl"):
            missing.append(issue_number)
            continue
        rank_by_url[normalize_href(post["postUrl"])] = rank

    if missing:
        values = ", ".join(f"#{number}" for number in missing)
        raise ValueError(f"自定义顺序中的文章不存在或未发布：{values}")
    return rank_by_url


def article_sort_key(article):
    rank = article["custom_rank"]
    if rank is not None:
        return (0, rank, "", article["original_index"])
    return (1, 0, article["date"], article["original_index"])


def find_date_label(text_node, row):
    tag = text_node.parent
    candidates = []
    while tag is not None and tag != row:
        if DATE_RE.fullmatch(tag.get_text(strip=True)):
            candidates.append(tag)
        tag = tag.parent
    return candidates[-1] if candidates else text_node.parent


def find_article_row(text_node):
    row = text_node.find_parent("a")
    if row is not None:
        return row
    return text_node.find_parent(
        class_=lambda value: value and "Box-row" in str(value)
    )


def set_custom_pin(row, is_pinned):
    icon_path = row.select_one("svg .svgTop0, svg .svgTop1")
    if icon_path is None:
        raise RuntimeError(f"文章行缺少置顶图标：{row.get('href', '')}")
    icon_path["class"] = ["svgTop1" if is_pinned else "svgTop0"]


def collect_articles(soup, rank_by_url):
    articles = []
    seen_rows = set()
    date_nodes = soup.find_all(
        string=lambda text: text is not None and DATE_RE.fullmatch(text.strip())
    )

    for text_node in date_nodes:
        row = find_article_row(text_node)
        if row is None or id(row) in seen_rows:
            continue
        seen_rows.add(id(row))
        href = normalize_href(row.get("href", ""))
        articles.append(
            {
                "date": text_node.strip(),
                "row": row,
                "date_label": find_date_label(text_node, row),
                "href": href,
                "custom_rank": rank_by_url.get(href),
            }
        )

    if not articles:
        raise RuntimeError("首页没有找到带日期的文章，为防止错误发布，构建已停止")
    return articles


def sort_articles(soup, articles):
    groups = defaultdict(list)
    for original_index, article in enumerate(articles):
        article["original_index"] = original_index
        article["parent"] = article["row"].parent
        groups[id(article["parent"])].append(article)

    for group in groups.values():
        group.sort(key=article_sort_key)
        first_row = min(group, key=lambda item: item["original_index"])["row"]
        marker = soup.new_tag("span")
        marker["data-gmeek-sort-marker"] = "true"
        first_row.insert_before(marker)
        for item in group:
            item["row"].extract()
        for item in group:
            marker.insert_before(item["row"])
        marker.decompose()


def process_homepage(root):
    from bs4 import BeautifulSoup

    index_file = root / "docs" / "index.html"
    order_file = root / "article-order.json"
    blog_base_file = root / "blogBase.json"
    if not index_file.exists():
        raise FileNotFoundError(f"{index_file} 不存在，无法继续部署")

    order = load_article_order(order_file)
    blog_base = json.loads(blog_base_file.read_text(encoding="utf-8"))
    rank_by_url = build_rank_by_url(order, blog_base)
    soup = BeautifulSoup(index_file.read_text(encoding="utf-8"), "html.parser")

    for link in soup.find_all("a", href=True):
        href = link.get("href", "").strip().lower()
        title = link.get("title", "").strip().lower()
        aria = link.get("aria-label", "").strip().lower()
        svg_text = str(link).lower()
        is_rss = (
            "rss.xml" in href
            or href.endswith("/rss")
            or href.endswith("/rss/")
            or title == "rss"
            or aria == "rss"
            or "octicon-rss" in svg_text
            or 'href="#rss"' in svg_text
            or 'href="#octicon-rss"' in svg_text
        )
        if is_rss:
            link["href"] = HOME_URL

    articles = collect_articles(soup, rank_by_url)
    for article in articles:
        set_custom_pin(article["row"], article["custom_rank"] is not None)
        article["date_label"].decompose()
    sort_articles(soup, articles)
    index_file.write_text(str(soup), encoding="utf-8")
    print(f"已处理 {len(articles)} 篇文章，自定义排序 {len(order)} 篇")


def verify_homepage(root):
    from bs4 import BeautifulSoup

    index_file = root / "docs" / "index.html"
    order = load_article_order(root / "article-order.json")
    blog_base = json.loads((root / "blogBase.json").read_text(encoding="utf-8"))
    rank_by_url = build_rank_by_url(order, blog_base)
    expected_urls = [url for url, _ in sorted(rank_by_url.items(), key=lambda item: item[1])]
    soup = BeautifulSoup(index_file.read_text(encoding="utf-8"), "html.parser")

    remaining_dates = [
        text.strip()
        for text in soup.find_all(string=True)
        if DATE_RE.fullmatch(text.strip())
    ]
    if remaining_dates:
        raise RuntimeError("首页仍然存在日期标签：" + ", ".join(remaining_dates[:10]))

    rows = soup.select("a.SideNav-item")
    actual_urls = [normalize_href(row.get("href", "")) for row in rows]
    if actual_urls[: len(expected_urls)] != expected_urls:
        raise RuntimeError("首页自定义文章顺序校验失败")

    for row, href in zip(rows, actual_urls):
        should_pin = href in rank_by_url
        is_pinned = row.select_one("svg .svgTop1") is not None
        if is_pinned != should_pin:
            raise RuntimeError(f"首页自定义置顶图标校验失败：{href}")

    print(f"已验证自定义顺序和图标，共 {len(expected_urls)} 篇，不限制数量")


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/opt/Gmeek")
    command = sys.argv[2] if len(sys.argv) > 2 else "process"
    if command == "process":
        process_homepage(root)
    elif command == "verify":
        verify_homepage(root)
    else:
        raise ValueError(f"未知命令：{command}")


if __name__ == "__main__":
    main()
