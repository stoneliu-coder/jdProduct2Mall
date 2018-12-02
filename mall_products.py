# !/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *;
from utils import *;
import numpy as np;
import pymysql;

class Mall_products:
    __isFirst = False;  
    __conn = '';
 
    @classmethod
    def get_connection(cls):
       
        if not cls.__isFirst:
            cls.__conn = pymysql.connect(host=Config.mysql.host,
                             user=Config.mysql.username,
                             password=Config.mysql.password,
                             charset='utf8mb4',
                             db=Config.mysql.db);
            cls.__isFirst = True;
        return cls.__conn;

    @classmethod
    def batch_excute_sql(cls,sql,params):
        conn = cls.get_connection();
        with conn.cursor() as cursor:
            try:
                cursor.executemany(sql,params);
                conn.commit();              
                # print_log(sql);
            except Exception,err:
                print_log('execute sql error:' + str(err));
            #cursor.close();
        #conn.close();

    @classmethod
    def excute_sql(cls,sql):
        conn = cls.get_connection();
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql);
                conn.commit();
            except Exception,err:
                print_log('execute sql err:' + str(err));

    @classmethod
    def add_categories(cls,categories):
        insert_sql = 'insert into himall_categories(Id,Name,DisplaySequence,ParentCategoryId,Depth,Path,HasChildren,TypeId,CommisRate,SafeStock,IsDelete) values(%s,%s,0,%s,%s,%s,%s,0,0,0,0);';
        params = [];
        for category in categories:
            param = [int(category['id']),category['name'],int(category['parent_id']),int(category['depth']),category['path'],int(category['has_child'])];
            params.append(param);
        cls.batch_excute_sql(insert_sql , params);

    @classmethod
    def empty_categories(cls):
        sql = 'delete from himall_categories';
        cls.excute_sql(sql);

    @classmethod
    def empty_products(cls):
        sql = 'delete from himall_skus;';
        cls.excute_sql(sql); 
        sql = 'delete from himall_shopProducts;';
        cls.excute_sql(sql);
        sql = 'delete from himall_products;';
        cls.excute_sql(sql);

    @classmethod
    def empty_shops(cls):
        sql = 'delete from himall_shops where id > 1';
        cls.excute_sql(sql);


    @classmethod
    def init_shops(cls):
        sql = 'insert into himall_shops(Id,GradeId,ShopName,IsSelf,ShopStatus,CreateDate,CompanyRegionId,CompanyEmployeeCount,CompanyRegisteredCapital,BusinessLicenceNumberPhoto,BankRegionId,Freight,FreeFreight,FranchiseeId,EnableDeliverGoods,OfflinePayEnable,IsBearIntegral,EnableSetStock,IsStoreDelive,IsAboveSelf,IsSetCommission,IsSetMemberRebate,OpenCashierShift,OpenPrintTicket,CashierDiscounts) values(%s,1,%s,1,7,"2018-11-20",102,100,1,"1",101,11,1,1,0,1,1,1,1,1,1,1,1,1,1)';
        params = [];
        for i in range(200):
            param = [str(i+2) , '测试门店' + str(i+1)];
            params.append(param);
        cls.empty_shops();
        cls.batch_excute_sql(sql,params);



    @classmethod
    def add_products(cls,products):
        sql = 'insert into himall_products(Id,ShopId,CategoryId,TypeId,BrandId,ProductName,SaleStatus,AuditStatus,AddedDate,DisplaySequence,MarketPrice,MinSalePrice,HasSKU,VistiCounts,SaleCounts,FreightTemplateId,EditStatus,Commission,IsGift,Deleted,SalesBase,RebateEnable,ProductSaleMethod,ProductSaleChannel,IsCompletelyDelete) values(%s,1,%s,0,0,%s,1,2,"2018-11-20",1,%s,%s,%s,1,1,0,1,0,0,0,0,1,0,1,0)';
        params = [];
        skus = [];
        descriptions = [];
        for product in products:
            param = [product['id'],product['cid'],product['name'],product['market_price'],product['min_sale_price'],product['has_sku']];
            params.append(param);
            skus = np.append(skus,product['skus']);

            description = [product['id'],product['id'],product['detail'],product['detail']];
            descriptions.append(description);
        cls.batch_excute_sql(sql,params);

        sql = 'insert into himall_productdescriptions(Id,ProductId,DescriptionPrefixId,DescriptiondSuffixId,Description,MobileDescription) values(%s,%s,0,0,%s,%s)';
        cls.batch_excute_sql(sql,descriptions);
        cls.add_skus(skus);
        cls.add_shop_products_skus(products);

    @classmethod
    def add_skus(cls,skus):
        sql = 'insert into himall_skus(Id,ProductId,Sku,Stock,CostPrice,SalePrice,AutoId,TopCategoryId,SafeStock,Specification1,Specification2,Specification3,Specification1Id,Specification2Id,Specification3Id) values(%s,%s,%s,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,%s,%s)';
        params = [];
        for sku in skus:
            param = [sku['id'],sku['product_id'],sku['sku'],sku['stock'],sku['cost_price'],sku['sale_price'],sku['auto_id'],sku['top_cid'],sku['sp1_value'],sku['sp2_value'],sku['sp3_value'],sku['sp1'],sku['sp2'],sku['sp3']];
            params.append(param);
        cls.batch_excute_sql(sql,params);


    @classmethod
    def add_shop_products_skus(cls,products):
        product_sql = 'insert into himall_shopproducts(ProductId,ShopId,FranchiseeId,State,SaleCount,Deleted,RebateEnable,Commission,Comments) values(%s,%s,1,1,100,0,0,0,0)';

        sku_sql = 'insert into himall_shopskus(ShopId,ProductId,SkuId,Stock,FranchiseeId,SupplyPrice,MinPrice,MaxPrice,SellingPrice) values(%s,%s,%s,%s,0,%s,%s,%s,%s)';
        shop_ids = cls.get_shop_ids();
        for shop_id in shop_ids:
            product_params = [];
            sku_params = [];
            for product in products:
                product_param = [product['id'],str(shop_id)];
                product_params.append(product_param);
                skus = product['skus'];
                for sku in skus:
                    sku_param = [str(shop_id),sku['product_id'],sku['auto_id'],sku['stock'],sku['cost_price'],sku['sale_price'],sku['sale_price'],sku['sale_price']];
                    sku_params.append(sku_param);
            cls.batch_excute_sql(product_sql,product_params);
            cls.batch_excute_sql(sku_sql,sku_params);

        


    @classmethod
    def get_shop_ids(cls):
        ids = [];
        for i in range(201):
            ids.append(i+1);
        return ids;


