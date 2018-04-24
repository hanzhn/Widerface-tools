
initstate = [0 100 256 512];
for i =1:1:3
    img1 = imread('/home/smiles/hz/databases/WIDER-face/WIDER_train/images/0--Parade/0_Parade_marchingband_1_5.jpg');
    [hpic,wpic] = size(img1);
    wpic=wpic/3
    hpic
    %-----------------------------------------Show the tracking result
    imshow(uint8(img1));
    rectangle('Position',initstate,'LineWidth',2,'EdgeColor','r');
    text(5, 18, strcat('#',num2str(i)), 'Color','y', 'FontWeight','bold', 'FontSize',20);
set(gcf,'PaperPositionMode','auto');
set(gca,'position',[0,0,1,1]);
set(gcf,'position',[1,1,wpic,hpic]);
    %保存结果
    %outputImg---文件夹
    outputImg = '/home/smiles/hz/';
    outputImgName = [outputImg,num2str(i),'.jpg'];
    saveas(gcf, outputImgName, 'jpg');
end