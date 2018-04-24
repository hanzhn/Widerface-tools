function [ dest ] = draw_rectangle( src, pt, wSize,  lineSize, color )
%简介：
% %将图像画上有颜色的框图，如果输入是灰度图，先转换为彩色图像，再画框图
% 图像矩阵
% 行向量方向  是  y
% 列向量方向  是  x
%----------------------------------------------------------------------
%输入：
% src：        原始图像，可以为灰度图，可为彩色图
% pt：         左上角坐标   [x1, y1]
% wSize：   框的大小      [wx, wy]
% lineSize： 线的宽度
% color：     线的颜色      [r,  g,  b]
%----------------------------------------------------------------------
%输出：
% dest：           画好了的图像
%----------------------------------------------------------------------

%判断输入参数个数
if nargin < 5
    color = [255 255 0];
end

if nargin < 4
    lineSize = 1;
end

if nargin < 3
    disp('输入参数不够 !!!');
    return;
end

[hpic, wpic, z] = size(src);
x1 = pt(1);
y1 = pt(2);
wx = wSize(1);
wy = wSize(2);
%如果是单通道的灰度图，转成3通道的图像
if 1==z
    dest(:, : ,1) = src;
    dest(:, : ,2) = src;
    dest(:, : ,3) = src;
else
    dest = src;
end

%开始画框图
for c = 1 : 3                 %3个通道，r，g，b分别画
    for dl = 1 : lineSize   %线的宽度，线条是向外面扩展的
        d = dl - 1;
        judge = [x1-d, y1-d, wpic, hpic]<=[0,0,x1+wx+d,y1+wy+d];
        A = [x1, y1, wx, wy]+judge.*[-x1+d+1,-y1+d+1,wpic-x1-wx-d,hpic-y1-wy-d];
        x1 = A(1);
        y1 = A(2);
        wx = A(3);
        wy = A(4);
        dest(  y1-d ,            (x1-d):(x1+wx+d) ,  c  ) =  color(c); %上方线条
        dest(  y1+wy+d ,    (x1-d):(x1+wx+d) ,  c  ) =  color(c); %下方线条
        dest(  (y1-d):(y1+wy+d) ,   x1-d ,           c  ) =  color(c); %左方线条
        dest(  (y1-d):(y1+wy+d) ,   x1+wx+d ,    c  ) =  color(c); %左方线条
    end
end %主循环尾

end %函数尾