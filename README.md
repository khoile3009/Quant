# Quant


There is 2 approach that can be done for datastreaming, after the configuraiton
- the next function will return the next interval and only allowing larger interval to be in consideration. 
    What if missing data -> Duplicate earlier
    Bigger interval will use the open from prev and aggregated high and low, close will be calculated with
    Only fetch the lcd of all required data. Have some form of converter to convert the required data tominimun data to fetch

    How to save data to local storage to not make it fetch many times - optimize for later

- Design decision:
    - rolling data and cut off through time