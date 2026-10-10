import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

def fraudcheck(): #you're going to be seeing how we handle highly unbalanced datasets in this function
    df = r.cc_data
    
    X = df.drop('Class', axis=1) #drop the 'Class' column from the dataset to create the feature set (X) and store it in a new variable. The 'Class' column is the target variable that indicates whether a transaction is fraudulent or not.
    y = df['Class'] 
    
    X_train, X_test, y_train, y_test = train_test_split( #split the dataset into training and testing sets, with 20% of the data reserved for testing. The stratify parameter ensures that the class distribution is preserved in both sets.
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    scaler = StandardScaler()  #scaler for the 'Amount' feature to standardize it, which can help improve model performance.
    X_train = X_train.copy()
    X_test = X_test.copy()
    
    X_train['Amount'] = scaler.fit_transform(X_train[['Amount']]) #extract data from the 'Amount' column, fit the scaler to it, and transform it to have a mean of 0 and a standard deviation of 1.
    X_test['Amount'] = scaler.transform(X_test[['Amount']])
    
    smote = SMOTE(random_state=42) #ok so smote is a technique that generates synthetic samples for the minority class to balance the dataset. It helps improve model performance on imbalanced datasets.
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    
    fraud_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    fraud_model.fit(X_train_res, y_train_res)
    
    y_prob = fraud_model.predict_proba(X_test)[:, 1]  #predict probabilities for the positive class (fraudulent transactions)
    
    return y_test.tolist(), y_prob.tolist() #return values 
