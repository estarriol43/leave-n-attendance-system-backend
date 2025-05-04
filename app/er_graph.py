
from sqlalchemy_schemadisplay import create_schema_graph
from database import engine, Base
from models import user, department, leave_type, leave_quota, leave_request, leave_request_attachment, notification

# 生成 ER 圖
graph = create_schema_graph(metadata=Base.metadata,
                            engine=engine, 
                            show_datatypes=True,  # 是否顯示數據類型
                            show_indexes=True,  # 是否顯示索引
                            rankdir='LR',  # 圖的方向，'TB' 為從上到下，'LR' 為從左到右
                            concentrate=False,
                            )  # 是否合併邊

# 儲存圖像
graph.write_png('database_relationship_graph.png')
