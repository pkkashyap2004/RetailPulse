"""Monthly naive forecast with a strictly chronological holdout."""
import pandas as pd
def evaluate_baseline(sales,holdout_months=3):
    f=sales.copy();f["date"]=pd.to_datetime(f.date)
    m=f.set_index("date").resample("MS").total_amount.sum().rename("actual").to_frame().asfreq("MS",fill_value=0)
    if len(m)<=holdout_months:raise ValueError("Need more monthly observations than holdout months")
    train,test=m.iloc[:-holdout_months],m.iloc[-holdout_months:].copy()
    test["forecast"]=float(train.actual.iloc[-1]);test["error"]=test.actual-test.forecast;test["absolute_error"]=test.error.abs()
    den=test.actual.abs().replace(0,pd.NA)
    return train,test,{"mae":float(test.absolute_error.mean()),"mape_pct":float((test.absolute_error/den).dropna().mean()*100) if den.notna().any() else None,"train_end":str(train.index[-1].date()),"test_start":str(test.index[0].date()),"test_end":str(test.index[-1].date()),"observations":len(m)}
