# Final Model Development Report

## Dataset Summary
- Number of samples: 7032
- Number of features: 10
- Positive churn rate: 0.2658

## Training Summary
- Models trained: 20
- Hyperparameter tuning method: RandomizedSearchCV
- Cross-validation strategy: StratifiedKFold with 5 folds

## Results Summary
          Model Name  Accuracy  Precision  Recall  F1 Score  ROC-AUC  CV Score  Training Time  Prediction Time
HistGradientBoosting    0.7953     0.6443  0.5134    0.5714   0.8380    0.8464           9.13           0.0141
            AdaBoost    0.7960     0.6526  0.4973    0.5645   0.8367    0.8434          10.26           0.0624
   Gradient Boosting    0.7896     0.6309  0.5027    0.5595   0.8365    0.8458          11.94           0.0030
 Stacking Classifier    0.7861     0.6237  0.4920    0.5501   0.8359    0.8456         133.92           0.0657
       Random Forest    0.7420     0.5095  0.7861    0.6183   0.8349    0.8431          31.00           0.1079
             XGBoost    0.7861     0.6151  0.5214    0.5644   0.8347    0.8459          15.87           0.0066
   Voting Classifier    0.7875     0.6214  0.5134    0.5622   0.8343    0.8438          11.36           0.0556
      MLP Classifier    0.7910     0.6325  0.5107    0.5651   0.8304    0.8407          41.54           0.0023
         Extra Trees    0.7285     0.4933  0.7861    0.6062   0.8303    0.8406          23.05           0.0928
 Logistic Regression    0.7846     0.6149  0.5080    0.5564   0.8303    0.8390           5.03           0.0056
      SGD Classifier    0.7832     0.6202  0.4759    0.5386   0.8300    0.8365           0.72           0.0021
          Linear SVM    0.7242     0.4885  0.7968    0.6057   0.8273    0.8379           0.37           0.0034
    Ridge Classifier    0.7242     0.4884  0.7914    0.6041   0.8256    0.8368           0.26           0.0040
             RBF SVM    0.6631     0.4324  0.8556    0.5745   0.8236    0.8344          66.40           0.3694
       Decision Tree    0.7804     0.6109  0.4786    0.5367   0.8167    0.8312           0.48           0.0016
         Gaussian NB    0.7178     0.4814  0.7941    0.5994   0.8166    0.8270           0.20           0.0026
        Bernoulli NB    0.7733     0.5676  0.6176    0.5915   0.8108    0.8179           0.33           0.0065
  Passive Aggressive    0.7491     0.5248  0.5936    0.5571   0.8046    0.7672           0.29           0.0030
                 KNN    0.7747     0.5947  0.4786    0.5304   0.8027    0.8135           0.89           0.0413
  Bagging Classifier    0.7640     0.5705  0.4545    0.5060   0.8004    0.8148          10.03           0.1331

## Best Model Analysis
- Selected model: HistGradientBoosting
- Best ROC-AUC: 0.8380
- Best F1 Score: 0.5714
- Best CV Score: 0.8464

## Feature Importance Analysis
                       Feature  Importance
                        tenure    0.064870
             Contract_Two year    0.062342
                MonthlyCharges    0.045102
   InternetService_Fiber optic    0.022133
             Contract_One year    0.014464
                  TotalCharges    0.005240
PaymentMethod_Electronic check    0.004833
               TechSupport_Yes    0.002752
            OnlineSecurity_Yes    0.002508
                       Partner   -0.000002

## Recommendations
- Deploy the saved joblib pipeline behind a batch or online inference service.
- Monitor calibration, data drift, and class-imbalance metrics over time.
- Re-train periodically with newly collected churn outcomes.