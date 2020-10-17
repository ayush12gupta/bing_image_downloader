import os
import shutil
import pandas as pd

try:
    from bing import Bing
except ImportError:  # Python 3
    from .bing import Bing


def download(query, limit=100, output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60):
    # engine = 'bing'
    if adult_filter_off:
        adult = 'off'
    else:
        adult = 'on'
    try:
        li = pd.read_csv('links.csv')
        link = li['Links'].to_list()
        fname = li['Files'].to_list()
        queries = li['Queries'].to_list()
        # start = fname.split('.')[0] + 1
    except:
        link = []
        fname = []
        queries = []
        # start = '1'
    cwd = os.getcwd()
    image_dir = os.path.join(cwd, output_dir, query)

    if force_replace:
        if os.path.isdir(image_dir):
            shutil.rmtree(image_dir)

    # check directory and create if necessary
    try:
        if not os.path.isdir("{}/{}/".format(cwd, output_dir)):
            os.makedirs("{}/{}/".format(cwd, output_dir))
    except:
        pass
    if not os.path.isdir("{}/{}/{}".format(cwd, output_dir, query)):
        os.makedirs("{}/{}/{}".format(cwd, output_dir, query))

    bing = Bing(query, limit, output_dir, adult, timeout, link, fname, queries)
    links, files, queries = bing.run()
    d = {'Files': files, 'Queries': queries, 'Links': links}
    lin = pd.DataFrame(d)
    if not os.path.exists("{}/{}".format(cwd, "links.csv")):
        lin.to_csv("{}/{}".format(cwd, "links.csv"))
    else:
        os.remove("{}/{}".format(cwd, "links.csv"))
        lin.to_csv("{}/{}".format(cwd, "links.csv"))


if __name__ == '__main__':
    download('abitabh', limit=10, timeout='1')
