import pandas as pd
import os
import logging
import argparse


class CustomerSegmentationUtils:
    """
    A helper class with static methods to facilitate
    the segmentation of customers based on their total purchases
    """

    @staticmethod
    def prepare_logging() -> logging.Logger:
        """
        Instantiates a logger object and sets the logging level to INFO

        Parameters:
        - input_logger_name (str): Name of logger to be created

        Returns:
        - logging.Logger: Logger object to be used
        """

        # setting current logging level to INFO
        logging.basicConfig(level=logging.INFO)

        # instantiating a logger object
        logger = logging.getLogger(__name__)

        # returning logger
        return logger

    @staticmethod
    def parse_arguments() -> argparse.Namespace:
        """
        Parses required and optional command line arguments

        Returns:
        - argparse.Namespace: An object containing the parsed arguments.
        """

        # preparing the argument parser
        parser = argparse.ArgumentParser(description='Customer Segmentation Argument Parser')

        # adding optional arguments to the parser
        parser.add_argument('--customer_id_column', type=str, default='customer_id',
                            help='Name of column that identifies different customers in data set')
        parser.add_argument('--purchase_amount_column', type=str, default='purchase_amount',
                            help='Name of column that identifies customer purchase amounts')
        parser.add_argument('--total_purchase_amount_column', type=str, default='total_purchase_amount',
                            help='Name of new column to be added, which will indicate total purchase amounts per customer')
        parser.add_argument('--customer_segment_column', type=str, default='customer_segment',
                            help='Name of new column to be added, which will indicate a customer"s segment, based on their total purchase amount')

        # returning the arguments, after being parsed
        args = parser.parse_args()
        return args

    @staticmethod
    def read_json_file(input_file_name: str) -> pd.DataFrame:
        """
        Reads json file data and loads into a pandas dataframe

        Parameters:
        - input_file_name (str): Name of source data json file

        Returns:
        - pd.DataFrame: Pandas dataframe containing file contents
        """
        # constructing data file path
        file_path = os.path.join('..', 'data', input_file_name)

        # reading data file into a data frame
        df = pd.read_json(file_path)

        # returning said dataframe
        return df

    @staticmethod
    def calculate_customer_total_purchase_amount(input_customer_data_df: pd.DataFrame, input_customer_id_column: str,
                                                 input_purchase_amount_column: str,
                                                 input_total_purchase_amount_column: str) -> pd.DataFrame:
        """
        Calculates total purchase amount per customer and returns as a separate pandas dataframe

        Parameters:
        - input_customer_data_df (pd.DataFrame): Dataframe containing customers and purchase amounts
        - input_customer_id_column (str): Name of column identifying individual customers
        - input_purchase_amount_column (str): Name of column indicating customer purchase amounts
        - input_total_purchase_amount_column (str): Name of new column, to indicate total purchase amount per customer

        Returns:
        - pd.DataFrame: Pandas dataframe containing customers and their total purchase amounts
        """
        # calculating the total purchase amounts per customer, and loading into a new dataframe
        customer_total_purchase_df = input_customer_data_df.groupby(input_customer_id_column)[
            input_purchase_amount_column].sum().reset_index()

        # renaming the purchase amount column
        customer_total_purchase_df = customer_total_purchase_df.rename(
            columns={input_purchase_amount_column: input_total_purchase_amount_column})

        # returning new dataframe
        return customer_total_purchase_df

    @staticmethod
    def segment_customer_data(input_customer_total_purchase_df: pd.DataFrame, input_customer_id_column: str,
                              input_total_purchase_amount_column: str,
                              input_customer_segment_column: str) -> pd.DataFrame:
        """
        Performs segmentation on customers, with respect to specifying total purchase amount ranges

        Parameters:
        - input_customer_total_purchase_df (pd.DataFrame): Dataframe containing customers and total purchase amounts
        - input_customer_id_column (str): Name of column identifying individual customers
        - input_total_purchase_amount_column (str): Name of column identifying total purchases for specific custoemrs
        - input_customer_segment_column (str): Name of column indicating customer segmentation

        Returns:
        - pd.DataFrame: Pandas dataframe containing customers, their total purchase amounts and which segment they fall
        under
        """
        # defining segmentation range filters depending on total purchase amounts
        segmentation_range_filters = [
            (input_customer_total_purchase_df[input_total_purchase_amount_column] < 100),
            (input_customer_total_purchase_df[input_total_purchase_amount_column] >= 100) & (
                    input_customer_total_purchase_df[input_total_purchase_amount_column] <= 500),
            (input_customer_total_purchase_df[input_total_purchase_amount_column] > 500)
        ]

        # defining the segmentation range labels to be assigned to customers
        segmentation_range_labels = ['Low', 'Medium', 'High']

        # preparing the updated dataframe
        customer_total_purchase_df = input_customer_total_purchase_df

        # checking for an empty data set
        if customer_total_purchase_df.empty:
            # if empty, then return the original data frame with an extra empty column representing the segments
            customer_total_purchase_df[input_customer_segment_column] = ''
            return customer_total_purchase_df

        # iterating through each segmentation filter, and assigning appropriate segmentation labels accordingly
        for segmentation_filter, segmentation_label in zip(segmentation_range_filters, segmentation_range_labels):
            customer_total_purchase_df.loc[segmentation_filter, input_customer_segment_column] = segmentation_label

        # converting the customer segment column into a categorical type
        customer_total_purchase_df[input_customer_segment_column] = pd.Categorical(
            customer_total_purchase_df[input_customer_segment_column],
            categories=['Low', 'Medium', 'High'],
            ordered=True
        )
        # sorting dataframe rows by label and customer id
        customer_total_purchase_df = customer_total_purchase_df.sort_values(
            by=[input_customer_segment_column, input_customer_id_column])

        # returning new dataframe
        return customer_total_purchase_df

    @staticmethod
    def print_dataframe(input_df: pd.DataFrame) -> None:
        """
        Prints a random 20 rows of an input dataframe

        Parameters:
        - input_df (pd.DataFrame): Dataframe to be printed

        Returns:
        - None
        """

        # removing the row numbers index column for enhanced presentation
        # printing 20 rows of the input dataframe
        pd.set_option('display.max_rows', 20)
        print(input_df.to_string(index=False))

    @staticmethod
    def write_csv_file(input_df: pd.DataFrame, input_file_name: str) -> None:
        """
        Reads pandas dataframe, and writes output to a csv file

        Parameters:
        - input_df (pd.DataFrame): Dataframe containing information to be written
        - input_file_name (str): Name of file to be written

        Returns:
        - None
        """
        # constructing data file path
        file_path = os.path.join('..', 'outputs', input_file_name)

        # writing dataframe to a csv file
        input_df.to_csv(file_path, index=False)
