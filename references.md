# Academic and Technical References

This document records the foundational research, algorithms, and benchmark citations utilized in the Logistics Data Analytics project. All sources are verified academic publications or industry standard textbooks.

---

## 1. Forecast Accuracy & Performance Evaluation

- **Hyndman, R. J., & Koehler, A. B. (2006).**
  - *Title:* Another look at measures of forecast accuracy.
  - *Journal:* International Journal of Forecasting, 22(4), 679–688.
  - *DOI / URL:* [https://doi.org/10.1016/j.ijforecast.2006.03.001](https://doi.org/10.1016/j.ijforecast.2006.03.001)
  - *Relevance:* Establishes mathematical definitions and criteria for forecasting metrics, addressing the numerical instability and asymmetric penalty of Mean Absolute Percentage Error (MAPE) under low or intermittent demand, justifying Weighted Absolute Percentage Error (WAPE) and Mean Absolute Scaled Error (MASE).

- **Croston, J. D. (1972).**
  - *Title:* Forecasting and stock control for intermittent demands.
  - *Journal:* Operational Research Quarterly, 23(3), 289–303.
  - *DOI / URL:* [https://doi.org/10.1057/jors.1972.50](https://doi.org/10.1057/jors.1972.50)
  - *Relevance:* Core formulation for intermittent demand decomposition (demand size vs. inter-arrival intervals) typical of slow-moving warehouse SKUs.

---

## 2. Inventory Classification & Management

- **Silver, E. A., Pyke, D. F., & Peterson, R. (1998).**
  - *Title:* Inventory Management and Production Planning and Scheduling (3rd ed.).
  - *Publisher:* John Wiley & Sons, New York.
  - *ISBN:* 978-0471119784
  - *Relevance:* Standard reference for multi-echelon inventory systems, safety stock determination under variable demand, and traditional ABC analysis (Pareto revenue contribution) combined with XYZ analysis (demand variability / coefficient of variation).

- **Scholz-Reiter, B., Heger, J., Meinecke, C., & Bergmann, J. (2012).**
  - *Title:* Integration of ABC and XYZ analysis with cluster analysis for inventory management.
  - *Book Chapter:* In Dynamics in Logistics (pp. 517–526). Springer, Berlin, Heidelberg.
  - *DOI / URL:* [https://doi.org/10.1007/978-3-642-32865-7_43](https://doi.org/10.1007/978-3-642-32865-7_43)
  - *Relevance:* Combines classical ABC/XYZ classification thresholds with unsupervised clustering (K-Means) to derive data-driven replenishment policies.

---

## 3. Machine Learning & Anomaly Detection

- **Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008).**
  - *Title:* Isolation Forest.
  - *Conference:* 2008 Eighth IEEE International Conference on Data Mining (ICDM), Pisa, Italy, pp. 413–422.
  - *DOI / URL:* [https://doi.org/10.1109/ICDM.2008.17](https://doi.org/10.1109/ICDM.2008.17)
  - *Relevance:* Theoretical basis for isolation-tree anomaly detection; isolates anomalies rather than profiling normal data points, enabling rapid detection of sudden demand surges, stock discrepancies, and recording outliers.

- **Friedman, J. H. (2001).**
  - *Title:* Greedy function approximation: A gradient boosting machine.
  - *Journal:* Annals of Statistics, 29(5), 1189–1232.
  - *DOI / URL:* [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451)
  - *Relevance:* Theoretical foundation for gradient boosted decision tree ensembles applied to tabular non-linear time-lag regression forecasting.

- **Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015).**
  - *Title:* Time Series Analysis: Forecasting and Control (5th ed.).
  - *Publisher:* John Wiley & Sons, Hoboken, NJ.
  - *ISBN:* 978-1118675922
  - *Relevance:* Methodological foundation for Autoregressive Integrated Moving Average (ARIMA) modeling, stationarity testing (Augmented Dickey-Fuller), and Akaike Information Criterion (AIC) model selection.

---

## 4. Vehicle Routing & Last-Mile Transportation

- **Toth, P., & Vigo, D. (Eds.). (2014).**
  - *Title:* Vehicle Routing: Problems, Methods, and Applications (2nd ed.).
  - *Series:* MOS-SIAM Series on Optimization, Society for Industrial and Applied Mathematics (SIAM), Philadelphia.
  - *DOI / URL:* [https://doi.org/10.1137/1.9781611973594](https://doi.org/10.1137/1.9781611973594)
  - *Relevance:* Comprehensive treatise on VRP formulations, exact integer linear programming algorithms, construction heuristics (e.g., Nearest Neighbor), and edge-exchange local improvement heuristics (e.g., Croes 2-Opt).

- **Croes, G. A. (1958).**
  - *Title:* A method for solving traveling-salesman problems.
  - *Journal:* Operations Research, 6(6), 791–812.
  - *DOI / URL:* [https://doi.org/10.1287/opre.6.6.791](https://doi.org/10.1287/opre.6.6.791)
  - *Relevance:* Original formulation of the 2-Opt local search edge-swapping heuristic for route untangling and total distance minimization.

- **Sinnott, R. W. (1984).**
  - *Title:* Virtues of the Haversine.
  - *Journal:* Sky and Telescope, 68(2), 159.
  - *Relevance:* Practical formulation of great-circle spherical distance computation between geographic latitude and longitude coordinates.
