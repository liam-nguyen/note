import os
import re
import codecs

# escape these directories when scanning
INVALID_DIR = {'figures', 'custom_theme', 'tags', 'css', '爬虫', 'Mila', 'Prob', 'APUE',
               'Projects', 'Tags', 'cpj', 'CSE521', 'Mila', 'Spark快速大数据分析'}

# escape these files when scanning
INVALID_FILES = {'目录.md'}

TOP = "/Users/larry/Documents/note/wiki/docs/"
TOP1 = "/Users/larry/Documents/note/"


class File:
    """
    文件
    """

    def __init__(self, name, path):
        """
        构建一个文件
        :param path: 文件路径, 绝对路径
        :param name: 文件名称
        """
        self.name = name
        self.path = path

    def is_hidden_file(self):
        """
        return true if the given file is a hidden file
        """
        return self.name.split("/")[-1].startswith(".")


    def is_md_file(self):
        """
        Is the file a markdown file?
        """
        return self.name[-3:] == '.md'


    def is_valid_folder(self):
        """
        Return true if the  given file is a valid folder
        """
        if not os.path.isdir(self.path):
            return False
        if self.is_hidden_file():
            return False
        if self.name in INVALID_DIR:
            return False
        return True

    def is_valid_file(self):
        """
        Return true if the  given file is either markdown file or a valid directory
        """
        if not self.is_md_file():
            return False
        if self.is_hidden_file():
            return False
        if self.name in INVALID_FILES:
            return False
        if self.is_hidden():
            return False
        return True

    def is_hidden(self):
        """
        Return true if the markdown file is hidden.
        """
        with codecs.open(self.path, mode='r') as file:
            for i in range(10):
                content = file.readline()
                if content.find("hidden") != -1:
                    if content.split(":")[1].strip().lower() == "true":
                        return True
        return False




class Item:
    """
    条目：可以是一本书，或者一个章节，或整个导航
    """

    def __init__(self, name, path):
        """
        :param name: 条目名称
        :param path: 条目路径，绝对路径
        """
        self.name = name
        self.path = path
        #  子条目
        self.items = []

    def add_item(self, item):
        """
        在该条目下添加一个子条目
        :param item: 子条目
        """
        self.items.append(item)
        return self

    def add_items(self, items):
        """
        在该条目下添加多个子条目
        :param items: 子条目列表
        """
        self.items.extend(items)
        return self

    def __contains__(self, item):
        """
        查询是否包含某个子条目
        :param item: 子条目
        :return: 是否包含该子条目
        """
        for _item in self.items:
            if _item == item:
                return True
        return False

    def __eq__(self, other):
        """
        判断条目是否相等
        :param other: 另一个条目
        :return: 条目是否相等
        """
        if self.name != other.name:
            return False
        if self.path != other.path:
            return False
        if set(self.items) != set(other.items):
            return False
        return True

    def print(self, level):
        """
        打印输出
        :param level: 第几级子条目，从0级开始
        :return: 字符串
        """
        s = level * "    " + "- '" + self.name + "':  '" + self.path + "'\n"
        if not self.items:
            return s
        for item in self.items:
            s += item.print(level+1)
        return s

    def __str__(self):
        return self.print(0)

    def type(self):
        """
        返回条目等级：1，2，3。。。
        """
        if not self.items:
            return 1
        else:
            return max(list(map(lambda item: item.type() + 1, self.items)))

    def traverse(self):
        """
        遍历文件夹，自动匹配、添加、生成子条目
        """
        for filename in os.listdir(self.path):
            filepath = os.path.join(self.path, filename)
            file = File(filename, filepath)
            if file.is_valid_file():
                self.add_item(Item(filename, filepath))
            elif file.is_valid_folder():
                item = Item(filename, filepath)
                item.traverse()
                self.add_item(item)
        self.sort_items()



    def sort_items(self):
        """
        两级排序：
        1. 根据条目等级排序，低等级的在前面
        2. 根据数字和字母顺序将每一级条目进行排序：升序
        """
        to_sort = []
        for item in self.items:
            # 排序：等级，数字，字母
            # 提取章节号
            item_number = re.search(r'\d+', item.name)
            if item_number:
                # 如果章节号存在
                digit = int(item_number.group())
            elif item.name == "index.md":
                # 特殊情况：把index.md 放在最前面
                digit= -9999
            else:
                 #没有章节号，放在后面
                digit = 0
                # 否则根据字母排序

            to_sort.append((item.type(), digit, item.name, item))
        to_sort.sort(key=lambda x: (x[0], x[1], x[2]))
        self.items = list(map(lambda x: x[3], to_sort))


    def generate_index(self):
        """
        生成index文件内容: 只适用于type=2
        """
        index_content = []
        for item in self.items:
            if item.name == 'index.md':  # 生成index不能包含自己
                continue
            # 根据条目等级，确定路径
            path = item.path.replace(TOP, '')
            start = [m.start() for m in re.finditer('/', path)][-self.type()] + 1
            index_content.append('* [%s](%s)\n' % (item.name.replace('.md', ''), path[start:]))
        index_content.append('\n')
        return ''.join(index_content)

    def generate_index_title(self, type):
        """
        index文件的标题, type来自self.type()
        """
        # 如果是总index的话，就不要标题了
        if self.name == "docs":
            return ""
        return (6 - type) * "#" + '  %s \n\n' % self.name

    def write_index(self):
        """
        将该条目写入到index文件中
        返回index文件内容
        """
        # 包含子条目吗？
        type = self.type()
        if type == 1:
            return '* [%s](%s)\n' % (self.name.replace('.md', ''), self.name)
        elif type == 2:
            # 只有几个条目，就不要有index了
            if len(self.items) < 4:
                return ""
            content = []
            # 对于每个子条目，也写入index文件中，并返回子条目的内容
            content = self.generate_index()
            with codecs.open(os.path.join(self.path, 'index.md'), 'w') as file:
                file.write(self.generate_index_title(3) + content)
                return self.generate_index_title(type) + content
        else:
            content = ""
            for item in self.items:
                content += item.write_index()
            with codecs.open(os.path.join(self.path, 'index.md'), 'w') as file:
                file.write(self.generate_index_title(4) + content)
                return self.generate_index_title(type) + content

    def yaml(self, level):
        """
        生成yaml条目
        """
        if self.type() == 1:
            s = level * "    " + "- '" + self.name.replace('.md', '') + "': '" + self.path.replace(TOP, "") + "'\n"

        else:
            s = level * "    " + "- '" + self.name + "': \n"

        # 剩余部分
        for item in self.items:
            s += item.yaml(level+1)
        return s

    def generate_yaml(self):
        """
        生成yaml目录
        :return:
        """
        s = ""
        for item in self.items:
            if item.name != "index.md":  # 自己就不要生成自己的index了
                s += item.yaml(0)
        return s


    def write_yml(self, ymlfile):
        """
        把条目写入yml文件中
        """
        old_contents = []  # 列表每一项代表文件中的每一行
        with codecs.open(ymlfile, mode='r', encoding='utf-8') as f:
            old_contents = f.read()
        # 寻找到nav标签，并且删除
        try:
            start_pos_of_nav = old_contents.index("nav:")
        except:   # nav:标签可能不存在
            start_pos_of_nav = len(old_contents)
        contents = old_contents[0:start_pos_of_nav]
        contents += ("nav:" + '\n')
        contents += self.generate_yaml()
        with codecs.open(ymlfile, mode='w', encoding='utf-8') as f:
            f.write(contents)

    def github(self, level):
        """
        生成github条目
        """
        s = ""
        if self.type() == 1:
            if self.name != "index.md":
                s += "* " + "[" + self.name.replace('.md', '') + "](" + \
                    self.path.replace(TOP1, "").replace(" ", "%20") + ")\n"
        else:
            s += "\n" + (level+2) * "#" + " " + self.name + "\n\n"

        # 剩余部分
        for item in self.items:
            s += item.github(level+1)
        return s

    def generate_github(self):
        """
        生成Github目录
        """
        s = "# 目录\n\n"
        for item in self.items:
            s += item.github(0)
        return s

    def write_github(self, readmefile):
        """
        生成Github的目录导航
        @:param filepath: 最后写入的文件
        1. 设置正确的地址
        2. 将空格替换成%20
        """
        with codecs.open(readmefile, mode='w', encoding='utf-8') as f:
            f.write(self.generate_github())


if __name__ == "__main__":
    blog_item = Item("docs", "/Users/larry/Documents/note/wiki/docs")
    blog_item.traverse()
    blog_item.write_index()
    blog_item.write_yml("/Users/larry/Documents/note/wiki/mkdocs.yml")
    blog_item.write_github( "/Users/larry/Documents/note/README.md")

















