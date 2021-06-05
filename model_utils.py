from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

def run_regression(X, y, test_size=0.3, random_state=19, show_score=False):
    '''
    Function creating a linear regression model and scoring it for training and testing data
    
    INPUT:
    X ... predctive features data
    y ... target data
    
    
    OUTPUT:
    r2_train_score ... r2 score for training data
    r2_test_score ... r2 score for test data
    '''
        
    #split the data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    #fit the model and obtain pred response
    linreg = LinearRegression(normalize=True)
    linreg.fit(X_train, y_train)
    y_test_preds = linreg.predict(X_test)
    y_train_preds = linreg.predict(X_train) 
    
    #calculate r2 scores
    r2_train_score = r2_score(y_train, y_train_preds)
    r2_test_score = r2_score(y_test, y_test_preds)
    
    if show_score == True:
        print('r2 score on training data: {:.2f}, r2 score on test data: {:.2f}'.format(r2_train_score, r2_test_score))
    
    return r2_train_score, r2_test_score

def find_best_score(df, relevant, y_target, start_with=1, step=1, test_size=.30, random_state=42, plot=True, show_score=False, negative_in_row_to_stop=10):
    '''
    Running liner regression using increasing number of features and returning best scores achieved
    '''
    cnt_negative=0
    r2_scores_test, r2_scores_train, num_feats = [], [], []
    
    for fcount in range(start_with, relevant.shape[0], step):
        X = df[relevant[:fcount].index]
        y = df[y_target]

        train_score, test_score = run_regression(X, y, show_score=show_score)    
        
        #store r2 score values    
        r2_scores_test.append(test_score)
        r2_scores_train.append(train_score)
        num_feats.append(fcount)        
        
        # stop the algortihms after the test score has been negative "dropping_in_row_to_stop" times in a row

        if test_score < 0:
            cnt_negative = cnt_negative + 1
        else:
            cnt_negative = 0
            
        if cnt_negative > negative_in_row_to_stop:
            break
        
                
    # Pick the best test score 
    best_test_index = r2_scores_test.index(max(r2_scores_test))
    
    train_score = r2_scores_train[best_test_index]
    test_score = r2_scores_test[best_test_index]
    no_features = num_feats[best_test_index]

    print("Best model with {} features: r2_score for training set {:.2f} and r2_score for test set {:.2f}".format(no_features, train_score, test_score))
    if plot:
        plt.rcParams["figure.figsize"] = [15, 10]
        plt.plot(num_feats[:no_features], r2_scores_test[:no_features], label="Test", alpha=.5)
        plt.plot(num_feats[:no_features], r2_scores_train[:no_features], label="Train", alpha=.5)
        plt.xlabel('Number of Features')
        plt.ylabel('Rsquared')
        plt.title('Rsquared by Number of Features')
        plt.legend(loc=2)        
        plt.show()
        
    return no_features, r2_scores_train, r2_scores_test, train_score, test_score

