%% Convert WIDERFACE annotation style to DARKNET style in txt files
%   Change the conditions to filter the annotation.

clear
set = {'train';'val'}

facenum = zeros(2,2);% to save the num of faces
piclistfile = fopen(strcat('data/WIDER_new-trainval.txt'), 'w+');
for ii=1:size(set)
load(strcat('/home/smiles/hz/databases/WIDER-face/annotation/wider_face_',set{ii},'.mat'));
for i=1:size(event_list)        
    %create label txt paths
    labelpath = strcat('WIDER_',set{ii},'/labels-new/', event_list{i}, '/')
    if ~exist(labelpath, 'dir')
        mkdir(labelpath);
    end
    for j=1:size(file_list{i})
        %get the widths and heights, write the pic names and pic paths to picpath txt
        jpgname = strcat('/home/smiles/hz/databases/WIDER-face/WIDER_',set{ii},'/images/',event_list{i},'/',file_list{i}{j},'.jpg');
        [hpic,wpic,~] = size(imread(jpgname));
        
        labelfile = fopen( strcat(labelpath,'/',file_list{i}{j},'.txt'), 'w+' );
        n = 0;
        for k=1:size(face_bbx_list{i}{j})
%             state = [blur_label_list{i}{j}(k), expression_label_list{i}{j}(k), illumination_label_list{i}{j}(k), invalid_label_list{i}{j}(k), occlusion_label_list{i}{j}(k), pose_label_list{i}{j}(k)];
%             difficult = sum([1.0,1.0,1.0,3.0,1.0,1.0].*double(state));
%             if difficult > 2.5
%                 continue;
%             end

            dw = 1.0/wpic;
            dh = 1.0/hpic;
            x = face_bbx_list{i}{j}(k,1);
            y = face_bbx_list{i}{j}(k,2);
            w = face_bbx_list{i}{j}(k,3);
            h = face_bbx_list{i}{j}(k,4);
            % 只要存在姿势不正常就去掉该照片
            if pose_label_list{i}{j}(k)>=1
                break;
            end
            if invalid_label_list{i}{j}(k)>=1 || occlusion_label_list{i}{j}(k)>=2 || w<45 || h<45
                continue;
            end
            x = (x+w/2)*dw;
            w = w*dw;
            y = (y+h/2)*dh;
            h = h*dh;
            if x>0 && x<1 && y>0 && y<1 && w>0 && w<1 && h>0 && h<1
                fprintf(labelfile, '0 %.12f %.12f %.12f %.12f\n', [x, y, w, h]);
                n = n+1;
                facenum(ii,2) = facenum(ii,2) + 1;
            end
        end
        
        fclose(labelfile);
        if n>=1%&& n<=30
            fprintf( piclistfile, strcat(jpgname,'\n') );
            facenum(ii,1) = facenum(ii,1) + 1;
        end
    end
end
end
fclose(piclistfile);
facenum
