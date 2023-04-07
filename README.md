# Horizontal_kinematic_constraints
绑定边界，模型的最左侧点和最右侧点相绑定自由度，可以模拟剪切箱效果

默认容差0.001，识别点靠容差

三维区分y向上或者z向上的情况，请注意甄别

需先划分好网格，并进入其他模块运行插件（在mesh里画网格后直接运行插件会报错，因为mesh信息未更新，所以需要进入其他模块才能正常读取网格信息）

判定同一高度的方式为纵坐标顺序，不看两侧坐标值，故两侧节点数必须相等。

将此文件夹放到C:\Users\你的用户名\abaqus_plugins\内，然后重启abaqus，即可

![1](https://user-images.githubusercontent.com/130127239/230577284-65c88ca0-8c4b-4d7b-bf9a-c8734be84201.png)
