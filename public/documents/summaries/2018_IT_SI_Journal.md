# Gone in 30 Days! Predictions for Car Import Planning

Everyone's eager to apply deep learning to forecasting, but when it comes to predicting car registrations for import planning in Austria, the lessons are more nuanced. This study pitted a state-of-the-art LSTM-RNN, a classic ARIMA-family (SARIMA) model, and a linear baseline head-to-head using monthly car registration data from 33 brands. The goal was to forecast next month's and the next year's registration demand, informing practical decisions on inventory and distribution for dealerships and importers.

**Key findings:**
- SARIMA consistently outperformed both the LSTM-RNN and the linear baseline across all error metrics (MAE, RMSE, MAPE, MASE) and both prediction horizons (monthly and annual).
- While LSTM-RNNs are powerful for long time series, the relatively short data sequences per brand (45-81 months) limited their advantage. SARIMA’s strength in handling explicit seasonality and trend, especially with structured car registration cycles, made it the better fit.
- The complexity of deep models didn’t translate to better accuracy—if anything, overfitting was a greater risk with LSTM given limited per-brand data.

A few nuances: SARIMA sometimes defaulted to the mean when it couldn’t find strong seasonality for niche brands, but these cases were exceptions. For market-leading brands with large volumes, percentage errors (MAPE) are the real target, while for niche brands, absolute errors (MAE) matter more in decision-making.

Bottom line: For car import planning scenarios with brand-level, seasonal time series, the classic approach is still king. If you’re itching to roll out deep learning, make sure the data volume and structure justify the complexity—or you’ll just be outperformed by a well-tuned SARIMA. This result fits with an emerging but under-appreciated trend: not every real-world forecasting setting is ready for deep nets, especially when the data just isn’t there.

[Download PDF](2018_IT_SI_Journal.pdf)
