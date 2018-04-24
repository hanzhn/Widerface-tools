% list = 0;
% for i = 1:size(blur_label_list)
%     for j = 1:size(blur_label_list{i,1})
%         a=size(blur_label_list{i,1}{j,1});
%         if list<a(1)
%             list = a(1)
%             i
%             j
%         end
%     end
% end
% list

img = imread('/home/smiles/hz/databases/WIDER-face/WIDER_train/images/1--Handshaking/1_Handshaking_Handshaking_1_234.jpg');
%i = rgb2gray(img);
% [hpic,wpic]=size(img);
% wpic = wpic/3
% hpic
% 
% x = 228
% y = 94
% w = 264
% h = 398
% x = (x + w/2)/wpic
% y = (y + h/2)/hpic
% w = w/wpic
% h = h/hpic
% 
% w = w*wpic
% h = h*hpic
% x = x*wpic
% y = y*hpic

k=11;
base = 20;
[hpic,wpic,~]=size(img);
y = floor(hpic/2);
x = floor(wpic/2);

% an = [1.08, 1.19;   3.42, 4.41;     6.63, 11.38;    9.42, 5.11;    16.62, 10.52];
% an = floor(an*base)
% for i=1:k
%     img = draw_rectangle(img,floor([x,y]-0.5*an(i,:)),an(i,:),2,[0,0,255]);
% end

% bn = [8.5498,10.0666;    2.4643,3.7665;    5.4841,7.6957;    1.1759,1.8197;    3.5097,5.4378];
%bn = [    6.5015    7.0309;    1.1370    1.7630;    2.3298    3.6676;    4.4452    9.0477;    8.9562   10.2477;    4.1334    4.6428;    2.8318    5.7710];
%bn = [    3.9574    4.4649;    3.2534    6.6067;    4.7590    9.6269;    9.4175   13.1415;    1.0372    1.6137;    6.0035    6.5331;    2.3505    4.6991;    2.2620    3.2312;    8.4844    8.9680];
bn = [    6.9917    7.6267
    2.1388    3.1102
   11.2284   13.7214
    2.2563    4.5087
    1.0139    1.5589
    5.6549   11.5328
    3.6573    4.1216
    3.0232    6.0962
    5.2112    5.7044
    4.1313    8.4068
    8.9787    9.4832];
bn = floor(bn*base)
for i=1:k
    img = draw_rectangle(img,floor([x,y]-0.5*bn(i,:)),bn(i,:),2,[255,0,0]);
end
imshow(img);



% f = fopen('test.txt', 'w+');
% fprintf(f, '0 %.12f %.12f %.12f %.12f\n', [1, 2, 3, 4])
% fclose(f)