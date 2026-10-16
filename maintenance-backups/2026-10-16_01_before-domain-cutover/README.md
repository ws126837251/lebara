# Lebara 使用指南 :link: https://tutorials.wufeng.de/lebara/

通过 GitHub Issues 编写和维护 Lebara 中文教程，使用 Gmeek 自动生成并部署到 GitHub Pages。

## 自定义首页文章顺序

编辑 `article-order.json` 中的 `order` 数组，按希望显示的先后顺序填写 GitHub Issue 编号：

```json
{
  "order": [3, 1, 17]
}
```

- 数量不限，数组中的文章会显示在首页最前面，并使用红色置顶图标。
- 未写入数组的文章会排在后面，并继续按发布日期从早到晚排序。
- 若要调整顺序，只需拖换编号位置；若要取消置顶，从数组中删除对应编号。
- 修改后提交到 `main`，工作流会自动重新生成并发布网站。

### Powered by :heart: [Gmeek](https://github.com/Meekdai/Gmeek)
