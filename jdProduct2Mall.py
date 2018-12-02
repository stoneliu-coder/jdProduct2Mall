#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
from config import *
from jd_products import *
from mall_products import *
import locale,sys

category_mapper = {u'0' : u'0'};
mall_categories_mapper = {};

def init_categories(write_to_db = False):
    categories = Jd_products.get_categories();
    global category_mapper;
    category_mapper = {u'0' : u'0'};
    global mall_categories_mapper;
    mall_categories_mapper = {};
    mall_categories = [];
    category_path = {};
    cid = 1;
    for category in categories:
        category_id = str(category['_id']);
        category_mapper.setdefault(category_id , cid);
        parent_id = str(category['parentId']);
        if parent_id == '0':
            category_path.setdefault(category_id , str(cid));
        else:
            category_path.setdefault(category_id , category_path[parent_id] + '|' + str(cid));
        mall_category = {
                          'id' : cid,
                          'name' : str(category['name']),
                          'parent_id' : category_mapper[parent_id],
                          'depth' : category['depth'],
                          'path' : category_path[category_id],
                          'has_child' : 1
                        };
        mall_categories.append(mall_category);
        mall_categories_mapper.setdefault(cid,mall_category);
        cid += 1;
    if write_to_db:
        Mall_products.empty_categories();
        Mall_products.add_categories(mall_categories);
        



def init_products(): 
    global category_mapper;
    products = Jd_products.get_products_by_category('9d1b4ba8966f4fa479e2734a610f9af9');

    sku_id = 1;
    product_id = 1;
    new_products = [];
    sps = [[1,2,3],[4,5,6],[7,8,9]];
    sps_values = [['白色','红色','黑色'],['小号','中号','大号'],['初级版','中级版','高级版']];
    for product in products:
        new_skus = [];
        skus = product['skus'];
        m = 0;
        p = 0;
        o = 0;
        cid = category_mapper[product['cid']];
        if skus and len(skus) > 0 :
            index = 0;
            sp1 = 0;
            sp2 = 0;
            sp3 = 0;
            for sku in skus:
                m = sku['m'];
                p = sku['p'];
                o = sku['op'];
                top_category = mall_categories_mapper[cid]['path'].split('|')[0];
                new_sku = {
                            'id':str(product_id) + '_' + str(sps[0][sp1]) + '_' +str(sps[1][sp2]) + '_' + str(sps[2][sp3]),
                            'product_id' : product_id,
                            'sku' : sku['skuId'],
                            'stock' : 1000,
                            'cost_price' : p,
                            'sale_price' : p,
                            'supply_price' : p,
                            'auto_id' : sku_id,
                            'top_cid' : top_category,
                            'sp1_value' : sps_values[0][sp1],
                            'sp2_value' : sps_values[1][sp2],
                            'sp3_value' : sps_values[2][sp3],
                            'sp1' : sps[0][sp1],
                            'sp2' : sps[1][sp2],
                            'sp3' : sps[2][sp3]
                          };
                sku_id += 1;
                new_skus.append(new_sku);

                sp3 += 1;
                if sp3 == 3:
                    sp3 = 0;
                    sp2 += 1;
                    if sp2 == 3:
                        sp2 = 0;
                        sp1 += 1;
                        if sp1 == 3:
                            break;



        new_product = {
                        'id' : product_id,
                        'cid' : cid,
                        'name' : product['pname'],
                        'market_price' : m,
                        'min_sale_price' : p,
                        'has_sku': True,
                        'skus' : new_skus,
                        'detail' : product['detail']
                      };
        product_id += 1;
        new_products.append(new_product);
    # Mall_products.empty_products();
    Mall_products.add_products(new_products);
    

    



if __name__ == '__main__':
    reload(sys) 
    sys.setdefaultencoding('utf-8')
    category_mapper = {};
    
    # empty_products();
    init_categories(True);
    init_products();
    # mall_products.init_shops();

