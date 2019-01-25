import pandas as pd
import numpy as np

def read_raw_data(file_name):
    inputfile = open(file_name, 'rb')
    dateParser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    data = pd.read_csv(inputfile,
                       usecols=['tpep_pickup_datetime',
                                'tpep_dropoff_datetime',
                                'passenger_count',
                                'trip_distance',
                                'PULocationID',
                                'DOLocationID',
                                'fare_amount'
                                ],
                       iterator= True,
                       dtype={'passenger_count':np.int,
                              'trip_distance':np.float,
                              'PULocation':np.int,
                              'DOLocation':np.int,
                              'fare_amount':np.float
                              },
                       parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'],
                       date_parser= dateParser,
                       na_filter=False,
                       )
    loop = True
    chunkSize = 10000
    chunks = []
    # i = 0  ### used in test, control the data size to read
    while loop:
        try:
            # i += 1
            # if i > 3:
            #     break
            chunk = data.get_chunk(chunkSize)
            chunks.append(chunk)
        except StopIteration:
            loop = False
    data = pd.concat(chunks, ignore_index = True)
    data = data[(data['PULocationID'] != data['DOLocationID']) & data['trip_distance']>0]
    # data = data[data['trip_distance']>0]
    print('here1')
    data['hour'] = \
        data.apply(lambda x: int(x['tpep_pickup_datetime'].hour), axis=1)
    data['pickup_time'] = \
        data.apply(lambda x: int(x['tpep_pickup_datetime'].hour * 60 + x['tpep_pickup_datetime'].minute), axis=1)
    ### original pickup time
    data['dropoff_time'] = \
        data.apply(lambda x: int(x['tpep_dropoff_datetime'].hour * 60 + x['tpep_dropoff_datetime'].minute), axis=1)
    data = data[data['dropoff_time'] > data['pickup_time']]
    data['travel_time'] = data['dropoff_time'] - data['pickup_time']
    data['day'] = data.apply(lambda x: x['tpep_pickup_datetime'].day, axis=1)
    # data['is_Served'] = 0
    data.drop(['tpep_pickup_datetime','tpep_dropoff_datetime'], axis=1, inplace=True)
    print('here2')
    data.to_csv('trip_data/filtered_yellow_tripdata_2018-01.csv', sep = ',', header = True, index = False)
    data.to_csv('trip_data/filtered_yellow_tripdata.csv', sep = ',', header = False, index = False, mode='a')
    inputfile.close()
'''
    data: DataFrame
    'day',
    'hour',
    'pickup_time',
    'dropoff_time',
    'travel_time',
    'passenger_count',
    'trip_distance',
    'PULocationID',
    'DOLocationID',
    'fare_amount'
'''

def read_filtered_data(file_name):
    inputfile = open(file_name, 'rb')
    data = pd.read_csv(inputfile,
                       usecols=['day',
                                'hour',
                                'pickup_time',
                                'dropoff_time',
                                'travel_time',
                                'passenger_count',
                                'trip_distance',
                                'PULocationID',
                                'DOLocationID',
                                'fare_amount',
                                ],
                       iterator= True,
                       dtype={'day':np.int,
                              'hour':np.int,
                              'pickup_time':np.int,
                              'dropoff_time':np.int,
                              'travel_time':np.int,
                              'passenger_count':np.int,
                              'trip_distance':np.float,
                              'PULocation':np.int,
                              'DOLocation':np.int,
                              'fare_amount':np.float
                              },
                       na_filter=False,
                       )
    loop = True
    chunkSize = 10000
    chunks = []
    # i = 0  ### used in test, control the data size to read
    while loop:
        try:
            # i += 1
            # if i > 2:
            #     break
            chunk = data.get_chunk(chunkSize)
            chunks.append(chunk)
        except StopIteration:
            loop = False
    data = pd.concat(chunks, ignore_index = True)
    inputfile.close()
    return data

'''
    data: DataFrame
    'day',
    'hour',
    'pickup_time',
    'dropoff_time',
    'travel_time',
    'passenger_count',
    'trip_distance',
    'PULocationID',
    'DOLocationID',
    'fare_amount'
'''

def read_request_data(file_name):
    inputfile = open(file_name, 'rb')
    data = pd.read_csv(inputfile,
                       usecols=['day',
                                'pickup_time',
                                'passenger_count',
                                'PULocationID',
                                'DOLocationID',
                                ],
                       iterator= True,
                       dtype={'day':np.int,
                              'pickup_time':np.int,
                              'passenger_count':np.int,
                              'PULocation':np.int,
                              'DOLocation':np.int,
                              },
                       na_filter=False,
                       )
    loop = True
    chunkSize = 10000
    chunks = []
    # i = 0  ### used in test, control the data size to read
    while loop:
        try:
            # i += 1
            # if i > 2:
            #     break
            chunk = data.get_chunk(chunkSize)
            chunks.append(chunk)
        except StopIteration:
            loop = False
    data = pd.concat(chunks, ignore_index = True)
    inputfile.close()
    return data

'''
    data: DataFrame
    'day',
    'pickup_time',
    'passenger_count',
    'PULocationID',
    'DOLocationID',
'''
# read_raw_data('trip_data/yellow_tripdata_2018-01.csv')
