#coding:utf8
import pandas as pd
import statsmodels.api as sm

def stepwise_selection(X,y,initial_list=[],threshold_in=0.05,threshold_out=0.10):
    """逐步回归降维法-基于P值"""
    included = list(initial_list)
    while True:
        changed = False
        excluded = list(set(X.columns) - set(included))
        new_pval = pd.Series(index=excluded)
        new_pval2 = pd.Series(index=excluded)
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included + [new_column]]))).fit()
            new_pval2[new_column] = model.pvalues[new_column]
            new_pval[new_column] = model.ess/model.ssr
        best_feature = new_pval.idxmax()
        best_pval = new_pval2[best_feature]
        if best_pval < threshold_in:
            included.append(best_feature)
            changed = True
            
        if not changed:
            break
    return included
