import numpy as np
from random import randint, choice
from trading_strategy_fitting import fit_strategy, offset_scan_validation, tic, underlined_output, import_data,\
    input_processing
from data_input_processing import  preprocessing_inputs
from strategy_evaluation import output_strategy_results


def random_search(strategy_dictionary_local, n_iterations):
    toc = tic()

    data_to_predict, data_2 = import_data(strategy_dictionary)
    fitting_inputs, continuous_targets, classification_targets = input_processing(
        data_to_predict, data_2, strategy_dictionary)

    counter = 0
    error = 1e5
    while counter < n_iterations:
        counter += 1
        strategy_dictionary_local = randomise_dictionary_inputs(strategy_dictionary_local)

        if strategy_dictionary['regression_mode'] == 'classification':
            fitting_targets = classification_targets
        elif strategy_dictionary['regression_mode'] == 'regression':
            fitting_targets = continuous_targets

        fitting_inputs = preprocessing_inputs(strategy_dictionary, fitting_inputs)

        fitting_dictionary, profit_factor = fit_strategy(strategy_dictionary_local, data_to_predict, data_2,
                                                         fitting_inputs, fitting_targets)
        error_loop = fitting_dictionary['error']

        if error_loop < error and fitting_dictionary['n_trades'] != 0:
            error = error_loop
            strategy_dictionary_local_optimum = strategy_dictionary_local
            fitting_dictionary_optimum = fitting_dictionary

    underlined_output('Best strategy fit')
    output_strategy_results(strategy_dictionary_local_optimum, fitting_dictionary_optimum, data_to_predict, toc)

    return strategy_dictionary_local_optimum


def randomise_dictionary_inputs(strategy_dictionary_local):
    strategy_dictionary_local['ml_mode'] = choice(['adaboost', 'randomforest', 'gradientboosting', 'extratreesfitting']) #'svm'
    strategy_dictionary_local['regression_mode'] = choice(['regression', 'classification'])
    strategy_dictionary_local['preprocessing'] = choice(['PCA', 'FastICA', 'None'])
    return strategy_dictionary_local


if __name__ == '__main__':
    strategy_dictionary = {
        'trading_currencies': ['USDT', 'BTC'],
        'ticker_1': 'USDT_BTC',
        'ticker_2': 'BTC_ETH',
        'scraper_currency_1': 'BTC',
        'scraper_currency_2': 'ETH',
        'candle_size': 1800,
        'n_days': 20,
        'offset': 0,
        'bid_ask_spread': 0.004,
        'transaction_fee': 0.0025,
        'train_test_ratio': 0.5,
        'output_flag': True,
        'plot_flag': False,
        'ml_iterations': 10,
        'target_score': 'idealstrategy',
        'windows': [10, 50, 100],
        'web_flag': True,
        'filename1': "USDT_BTC.csv",
        'filename2': "BTC_ETH.csv",
        'scraper_page_limit': 20,
    }

    search_iterations = 50

    strategy_dictionary = random_search(strategy_dictionary, search_iterations)

    underlined_output('Offset validation')
    offsets = np.linspace(0, 300, 5)

    offset_scan_validation(strategy_dictionary, offsets)

    print strategy_dictionary
