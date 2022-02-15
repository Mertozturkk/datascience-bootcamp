import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import logging


class DataOperations(object):
    """
    This class is used to perform operations on the data.
    """
    DATA_COUNT, LOW, HIGH = 1000, 0, 100

    def __init__(self, data=None):
        """
        This is the constructor of the class.
        :param data:
        """
        if data is None:  # if no data is given, create random data
            Default_data_frame = pd.DataFrame(
                self._create_data(DataOperations.DATA_COUNT, DataOperations.LOW, DataOperations.HIGH),
                columns=["x1", "y", "Label"])
            self.dataframe_info(Default_data_frame)
        else:  # if data is given, create dataframe from data
            data_frame = self.create_df_from_data(data)
            logging.info("DataFrame created")
            self.dataframe_info(data_frame)
            self.dataframe_histogram(data_frame)

    def create_df_from_data(self, data):
        """
        This method creates a dataframe from the given data.
        :param data (user given data):
        :return dataframe:
        """
        if type(data).__module__.split(".")[0] == "pandas":  # if data is a pandas dataframe
            return data
        if type(data) is str:
            path = data  # path to (csv |json |xlsx) file
            path_type = path.split(".")[-1]  # check if file type is csv | json | xlsx
            if path_type == "csv":
                pandas_object_csv = pd.read_csv(path)
                return pandas_object_csv
            elif path_type == "json":
                pandas_object_json = pd.read_json(path)
                return pandas_object_json
            elif path_type == "xlsx":
                pandas_object_xlsx = pd.read_excel(path)
                return pandas_object_xlsx
            else:
                raise ValueError("File type not supported")
        elif type(data).__module__ == "numpy":  # if data is a numpy array
            column_name_list = []
            columns_size = len(data[0])
            for _ in range(columns_size):  # create column names
                column_name = "Column_" + str(_)
                column_name_list.append(column_name)
            pandas_object_from_numpy = pd.DataFrame(data=data, columns=column_name_list)
            return pandas_object_from_numpy

    @classmethod
    def _create_data(cls, number_of_data: int, low_value: int, high_value: int) -> DataFrame:
        """
        This method creates random data.
        :param number_of_data:
        :param low_value:
        :param high_value:
        :return:
        """
        data = []
        for _ in range(number_of_data):
            x1 = np.random.randint(low=low_value, high=high_value)
            y = np.random.randint(low=low_value, high=high_value)
            label = "1" if x1 > y else "0"
            data.append([x1, y, label])
        df = pd.DataFrame(data=data, columns=["x1", "y", "Label"])
        return df

    def dataframe_info(self, dataframe: DataFrame):
        """
        This method gives some information about the dataframe
        :param dataframe:
        :return:
        """
        logging.info("Dataframe info:")
        dataframe.info(verbose=True)
        print("\n")
        dataframe.describe()
        for i in range(0, len(dataframe.columns.values)):
            if dataframe[dataframe.columns[i]].dtype == "int64" or dataframe[dataframe.columns[i]].dtype == "float64":
                logging.info("Some statistics for column: " + dataframe.columns[i])
                logging.info("Dataframe %s info:", dataframe.columns[i])
                plt.hist(dataframe[dataframe.columns[0]], bins=100)
                plt.show()
                dataframe[dataframe.columns[i]].info(verbose=True)
                print("\n")
                dataframe[dataframe.columns[i]].describe()

    def dataframe_histogram(self, dataframe: DataFrame):
        """
        This method creates histograms for all columns in the dataframe.
        :param dataframe:
        :return:
        """
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_numerics_only = dataframe.select_dtypes(include=numerics)
        try:
            if len(df_numerics_only.columns) > 1 and ((dataframe[dataframe.columns[0]].dtype == "int64") or (
                    dataframe[dataframe.columns[0]].dtype == "float64") and (
                                                              dataframe[dataframe.columns[1]].dtype == "int64") or
                                                      dataframe[dataframe.columns[1]].dtype == "float64"):
                # if dataframe has more than one column and both columns are int64 or float64
                data_num = list(dataframe.count())[0]
                colors = np.random.rand(data_num)
                area = (30 * np.random.rand(data_num)) ** 2

                plt.scatter(dataframe[dataframe.columns[0]], dataframe[dataframe.columns[1]], s=area, c=colors,
                            alpha=0.5)
                plt.show()
                df_numerics_only.plot(kind='box', subplots=True, layout=(1, len(df_numerics_only.columns)),
                                      sharex=False, sharey=False)
                plt.show()
        except Exception as e:
            logging.warning("first two columns of your dataset must be numeric")
