import unittest
import pandas as pd
from src.utils import CustomerSegmentationUtils as csu


class TestCustomerSegmentationUtils(unittest.TestCase):
    """
    A series of test cases for some methods defined in the CustomerSegmentationUtils class.
    """
    def assert_pd_df_equal_ignore_index(self, left, right):
        """
        Implementing a separate function to facilitate pandas data frame comparisons without indices having to be equal
        """
        pd.testing.assert_frame_equal(left.reset_index(drop=True), right.reset_index(drop=True))


    def test_calculate_customer_total_purchase_amount_standard(self):
        """
        Testing that the calculate_customer_total_purchase_amount function performs the groupings and totals correctly
        """
        # setting up the test input data frame
        input_df = pd.DataFrame({'customer_id': [1, 2, 1], 'purchase_amount': [100, 200, 300]})

        # setting up the expected output data frame
        expected_output_df = pd.DataFrame({'customer_id': [1, 2], 'total_purchase_amount': [400, 200]})

        # obtaining the total purchase amounts using the function
        output_df = csu.calculate_customer_total_purchase_amount(
            input_customer_data_df=input_df, input_customer_id_column='customer_id', input_purchase_amount_column='purchase_amount',
            input_total_purchase_amount_column='total_purchase_amount'
        )

        # verifying that the correct totals and groupings are obtained
        self.assert_pd_df_equal_ignore_index(output_df, expected_output_df)

    def test_calculate_customer_total_purchase_amount_empty_data(self):
        """
        Testing that the calculate_customer_total_purchase_amount function can pass when the loaded data frame is empty
        """
        # setting up the empty test input data frame
        input_df = pd.DataFrame(columns=['customer_id', 'purchase_amount'])

        # setting up the expected empty output data frame
        expected_output_df = pd.DataFrame(columns=['customer_id', 'total_purchase_amount'])

        # obtaining the total purchase amounts using the function, which should return empty here
        output_df = csu.calculate_customer_total_purchase_amount(
            input_customer_data_df=input_df, input_customer_id_column='customer_id', input_purchase_amount_column='purchase_amount',
            input_total_purchase_amount_column='total_purchase_amount'
        )

        # verifying that both data frames are equal, as expected
        self.assert_pd_df_equal_ignore_index(output_df, expected_output_df)

    def test_segment_customer_data_standard(self):
        """
        Testing that the segment_customer_data function performs the segmentation logic correctly
        """
        # setting up the test input data frame
        input_df = pd.DataFrame({'customer_id': [1, 2, 3], 'total_purchase_amount': [50, 150, 600]})

        # setting up the expected output data frame
        expected_output_df = pd.DataFrame({'customer_id': [1, 2, 3], 'total_purchase_amount': [50, 150, 600],
                                           'customer_segment': pd.Categorical(['Low', 'Medium', 'High'],
                                                                              categories=['Low', 'Medium', 'High'],
                                                                              ordered=True)})

        # performing the segmentation logic on the customers, based on their total purchase amounts
        output_df = csu.segment_customer_data(
            input_customer_total_purchase_df=input_df, input_customer_id_column='customer_id',
            input_total_purchase_amount_column='total_purchase_amount', input_customer_segment_column='customer_segment'
        )

        # verifying that the correct segmentation labels are assigned
        self.assert_pd_df_equal_ignore_index(output_df, expected_output_df)

    def test_segment_customer_data_empty_data(self):
        """
        Testing that the segment_customer_data function can pass when the loaded data frame is empty
        """
        # setting up the empty test input data frame
        input_df = pd.DataFrame(columns=['customer_id', 'total_purchase_amount'])

        # setting up the expected empty output data frame
        expected_output_df = pd.DataFrame(columns=['customer_id', 'total_purchase_amount', 'customer_segment'])

        # performing the segmentation logic on empty data
        output_df = csu.segment_customer_data(
            input_customer_total_purchase_df=input_df, input_customer_id_column='customer_id',
            input_total_purchase_amount_column='total_purchase_amount', input_customer_segment_column='customer_segment'
        )

        # verifying that both data frames are equal, as expected
        self.assert_pd_df_equal_ignore_index(output_df, expected_output_df)
