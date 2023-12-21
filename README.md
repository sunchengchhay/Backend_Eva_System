# FE_System_Backend

# setup
1. download environment:
    Mac: python3 -m venv env
    
2. activate env
    Mac: source env/bin/activate

3. install all libraries in requirements.txt after activate env
    Mac: pip3 install -r requirements.txt

4. after download sucess all libraries run this command
    Mac: python3 run.py

5. if you see message like this module "flask.scaffold" not found
    go and config in env folder , try to find filen flask-restx/api.py in line 17-20 replace it with below code
   
    try:
        from flask.helpers import _endpoint_from_view_func
    except ImportError:
        from flask.sansio.scaffold import _endpoint_from_view_func

7. after this , run : python3 run.py again , it works now
