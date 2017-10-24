# coding: utf-8
import os

import MySQLdb
import csv
import sys

class WikipediaHelper:
    @staticmethod
    def fetch_cat(cursor, cat_title):
        sql = 'select cat_id, cat_title from category where cat_title = %s'
        cursor.execute(sql, args=[cat_title.encode('utf-8')])
        for row in cursor.fetchall():
            return {'cat_id': row[0], 'cat_title': row[1].decode('utf-8'), 'parent_cat_id': ''}

    @staticmethod
    def fetch_and_write_cat(cursor, cat_hash, writer , s=set()):
        l = len(s)
        s.add('%d_%s' % (cat_hash['cat_id'], cat_hash['parent_cat_id']))
        if l == len(s):
            return
        # write category
        print('write category %s' % cat_hash)
        writer.writeline(cat_hash)
        sql = 'select cat2.cat_id, page.page_title from categorylinks ' \
              'join page on page.page_id = categorylinks.cl_from ' \
              'join category on categorylinks.cl_to = category.cat_title ' \
              'inner join category as cat2 on cat2.cat_title = page.page_title ' \
              'where categorylinks.cl_type = \'subcat\' and category.cat_title = %s and page.page_title <> %s;'
        cursor.execute(sql,
                       args=
                       [
                           cat_hash['cat_title'].encode('utf-8'),
                           cat_hash['cat_title'].encode('utf-8'),
                       ])
        for row in cursor.fetchall():
            childhash = {'cat_id': row[0], 'cat_title': row[1].decode('utf-8'), 'parent_cat_id': cat_hash['cat_id']}
            WikipediaHelper.fetch_and_write_cat(cursor=cursor, cat_hash=childhash, writer=writer, s=s)


class CsvSaver:
    def __init__(self):
        pass

    def set_filepath(self, filepath):
        self.filepath = filepath

    def set_header(self, header):
        self.header = header

    def init(self):
        if os.path.isfile(self.filepath):
            os.remove(self.filepath)

        self.f = open(self.filepath, 'w')
        self.w = csv.DictWriter(self.f, self.header)
        self.w.writeheader()

    def writeline(self, hash):
        self.w.writerow(hash)

    def finalize(self):
        self.f.close()

def main():
    # for stack overflow measure
    sys.setrecursionlimit(20000)

    conn = MySQLdb.connect(
        user='root',
        passwd='',
        host='localhost',
        db='wikipedia'
    )
    c = conn.cursor()

    # 1. init writer
    writer = CsvSaver()
    writer.set_header(('cat_id', 'cat_title', 'parent_cat_id'))
    writer.set_filepath('/opt/categories.csv')
    writer.init()

    # 1. fetch root category
    print('fetch root category')
    root_cat = WikipediaHelper.fetch_cat(c, '主要カテゴリ')
    # 2. fetch and writer category recursively
    WikipediaHelper.fetch_and_write_cat(cursor=c, cat_hash=root_cat, writer=writer)

    c.close()
    conn.close()


if __name__ == '__main__':
    main()
