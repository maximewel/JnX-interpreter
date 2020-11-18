
for %%f in (data\*.jnx) 
    do ( 
        python .\parserast.py %%f
    )