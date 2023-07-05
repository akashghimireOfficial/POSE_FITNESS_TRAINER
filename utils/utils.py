import yaml


def read_yaml(yaml_path):

    with open(yaml_path,'r') as file:
        joint_config=yaml.safe_load(file)
    return joint_config


def fall_detection(p1,p2):
    x_min,y_min=p1
    x_max,y_max=p2
    h=y_max-y_min
    w=x_max-x_min

    if w>h:
       
        return True
    else:
        return False
    


