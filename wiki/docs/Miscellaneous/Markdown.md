---
title: Markdown
toc: true
date: 2017-10-30
tags: [Markdown]
---

#### Pandoc

[Pandoc](https://pandoc.org)可以方便的转换Markdown格式。其中一个最有用的功能是多个md文件生成pdf文档。

```bash
pandoc --toc -o book.pdf title.txt *.md --pdf-engine=xelatex 
```

其中title.text是pdf文档的题目信息

```md
---
title: Getting Started Guide
author: Fernando B.
rights: Nah
language: en-US
---
```

但是默认产生的PDF文档不太美观。幸运的是，[PanBook](https://github.com/annProg/PanBook)已经为中文PDF制作了优美的主题。