import pandas as pd


data = pd.read_csv('business.csv')
print(data.columns)

data = data.rename(columns = {  #подготовка данных
    'Product Type' : 'product_type',
    'Net Quantity' : 'net_quantity',
    'Gross Sales' : 'gross_sales',
    'Discounts' : 'discounts',
    'Returns' : 'returns',
    'Total Net Sales' : 'total_net_sales'})
                                 #получение результата
product_quant = data.query('returns == 0')\
      .groupby('product_type', as_index=False)\
      .aggregate({'net_quantity': 'sum'})\
      .sort_values('net_quantity', ascending=False)

product_quant.to_csv('product_quantity.csv', index = False)