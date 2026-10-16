import json
import tempfile
import unittest
from pathlib import Path

from scripts.customize_homepage import (
    article_sort_key,
    build_rank_by_url,
    load_article_order,
    normalize_href,
    process_homepage,
    verify_homepage,
)


class ArticleOrderTests(unittest.TestCase):
    def test_accepts_more_than_three_articles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "article-order.json"
            path.write_text(json.dumps({"order": [9, 7, 5, 3, 1]}), encoding="utf-8")
            self.assertEqual(load_article_order(path), [9, 7, 5, 3, 1])

    def test_rejects_duplicate_issue_numbers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "article-order.json"
            path.write_text(json.dumps({"order": [3, 1, 3]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "重复"):
                load_article_order(path)

    def test_maps_issue_numbers_to_exact_article_order(self):
        blog_base = {
            "postListJson": {
                "P1": {"postUrl": "post/one.html"},
                "P3": {"postUrl": "post/%E4%B8%89.html"},
                "P17": {"postUrl": "post/seventeen.html"},
            }
        }
        ranks = build_rank_by_url([3, 1, 17], blog_base)
        self.assertEqual(ranks, {"post/三.html": 0, "post/one.html": 1, "post/seventeen.html": 2})

    def test_sort_places_all_configured_articles_first(self):
        articles = [
            {"custom_rank": None, "date": "2026-01-01", "original_index": 0},
            {"custom_rank": 3, "date": "2026-01-05", "original_index": 1},
            {"custom_rank": 0, "date": "2026-01-06", "original_index": 2},
            {"custom_rank": None, "date": "2026-01-02", "original_index": 3},
        ]
        result = sorted(articles, key=article_sort_key)
        self.assertEqual([item["custom_rank"] for item in result], [0, 3, None, None])

    def test_normalizes_site_and_encoded_urls(self):
        self.assertEqual(
            normalize_href("https://tutorials.wufeng.de/lebara/post/%E6%B5%8B%E8%AF%95.html?x=1"),
            "post/测试.html",
        )

    def test_processes_unlimited_order_and_pin_icons(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            order = [5, 4, 3, 2, 1]
            (root / "article-order.json").write_text(
                json.dumps({"order": order}), encoding="utf-8"
            )
            posts = {
                f"P{number}": {"postUrl": f"post/{number}.html"}
                for number in range(1, 7)
            }
            (root / "blogBase.json").write_text(
                json.dumps({"postListJson": posts}), encoding="utf-8"
            )
            rows = "".join(
                f'<a class="SideNav-item" href="post/{number}.html">'
                '<svg><path class="svgTop0"></path></svg>'
                f'<span class="Label">2026-01-0{number}</span>文章{number}</a>'
                for number in range(1, 7)
            )
            (root / "docs" / "index.html").write_text(
                f"<html><body><nav>{rows}</nav></body></html>", encoding="utf-8"
            )

            process_homepage(root)
            verify_homepage(root)

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(
                (root / "docs" / "index.html").read_text(encoding="utf-8"),
                "html.parser",
            )
            actual = [row["href"] for row in soup.select("a.SideNav-item")]
            self.assertEqual(actual, [f"post/{number}.html" for number in [5, 4, 3, 2, 1, 6]])


if __name__ == "__main__":
    unittest.main()
