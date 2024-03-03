from utils import CustomerSegmentationUtils as csu

# setting up logging
logger = csu.prepare_logging()

def main():
    # parsing command line arguments
    logger.info('Parsing command line arguments')
    args = csu.parse_arguments()

    # accessing arguments
    customer_id_column = args.customer_id_column
    purchase_amount_column = args.purchase_amount_column
    total_purchase_amount_column = args.total_purchase_amount_column
    customer_segment_column = args.customer_segment_column

    # reading customer data into a dataframe
    logger.info('Reading customer data from input file')
    customer_data_df = csu.read_json_file(input_file_name='CustData.json')

    # calculating total purchase amount per customer
    logger.info('Calculating total purchase amount per customer')
    customer_total_purchase_df = csu.calculate_customer_total_purchase_amount(
        input_customer_data_df=customer_data_df,
        input_customer_id_column=customer_id_column,
        input_purchase_amount_column=purchase_amount_column,
        input_total_purchase_amount_column=total_purchase_amount_column
    )

    # implementing customer segmentation based on total purchase amounts
    logger.info('Implementing customer segmentation based on purchase amounts')
    segmented_customer_total_purchase_df = csu.segment_customer_data(
        input_customer_total_purchase_df=customer_total_purchase_df,
        input_customer_id_column=customer_id_column,
        input_total_purchase_amount_column=total_purchase_amount_column,
        input_customer_segment_column=customer_segment_column
    )

    # printing some sample rows of the final dataframe
    logger.info('Listing sample rows of final data set')
    csu.print_dataframe(input_df=segmented_customer_total_purchase_df)

    # writing the customer segmentation information to a csv file
    logger.info('Writing data set to a csv file')
    csu.write_csv_file(input_df=segmented_customer_total_purchase_df, input_file_name='CustSeg.csv')

if __name__ == "__main__":
    main()
