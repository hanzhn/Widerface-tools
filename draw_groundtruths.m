% draw the groundtruths on pics for WIDER-face
clear
set = {'train';'val'};

facenum = zeros(2,2);% to save the num of faces
for ii=1:size(set)
    % loop items of set
    load(strcat('/home/smiles/hz/databases/WIDER-face/annotation/wider_face_',set{ii},'.mat'));    
    
    for i=1:size(event_list)
        % create save paths
        savepath = strcat('groundtruths_',set{ii},'/', event_list{i}, '/')
        if ~exist(savepath, 'dir')
            mkdir(savepath);
        end
        
        for j=1:size(file_list{i})
            % get the widths and heights, write the pic names and pic paths to picpath txt
            jpgname = strcat('/home/smiles/hz/databases/WIDER-face/WIDER_',set{ii},'/images/',event_list{i},'/',file_list{i}{j},'.jpg')
            img1 = imread(jpgname);
            [hpic,wpic,~] = size(img1);
            
            for k=1:size(face_bbx_list{i}{j})
                x = floor( face_bbx_list{i}{j}(k,1) );
                y = floor( face_bbx_list{i}{j}(k,2) );
                w = floor( face_bbx_list{i}{j}(k,3) );
                h = floor( face_bbx_list{i}{j}(k,4) );
                %判断框的边界问题
                if x>wpic || y>hpic
                    disp('画的框将不在图像范围内！');
                    continue;
                end
                if x<0
                    x = 0;
                end
                if y<0
                    y = 0;
                end
                if (x+w)>wpic
                    w = wpic-x;
                end
                if (y+h)>hpic
                    h = hpic-y;
                end
                
                % delete hard faces
%                 state = [blur_label_list{i}{j}(k), expression_label_list{i}{j}(k), illumination_label_list{i}{j}(k), invalid_label_list{i}{j}(k), occlusion_label_list{i}{j}(k), pose_label_list{i}{j}(k)];
%                 difficult = sum([1.0,1.0,1.0,3.0,1.0,1.0].*double(state));
%                 if difficult > 2.5opencv
%                     disp('too difficult!!');
%                     img1 = draw_rectangle(img1,[x,y],[w,h],2,[0,255,0]);
%                     continue;
%                 end
                state = [blur_label_list{i}{j}(k), expression_label_list{i}{j}(k), illumination_label_list{i}{j}(k), occlusion_label_list{i}{j}(k), pose_label_list{i}{j}(k), invalid_label_list{i}{j}(k)];
                if sum(state)==0
                    img1 = draw_rectangle(img1,[x,y],[w,h],2,[0,255,255]);
                else
                    if state(1)>0
                        if state(1)==1
                            img1 = draw_rectangle(img1,[x,y],[w,h],2,[255,0,0]);
                        else
                            img1 = draw_rectangle(img1,[x,y],[w,h],2,[153,0,0]);
                        end
                    end
                    if state(2)>0
                        img1 = draw_rectangle(img1,[x,y],[w+2,h+2],2,[0,0,255]);     
                    end
                    if state(3)>0
                        img1 = draw_rectangle(img1,[x,y],[w+4,h+4],2,[255,255,0]); 
                    end
                    if state(4)>0
                        if state(4)==1
                            img1 = draw_rectangle(img1,[x,y],[w+6,h+6],2,[0,255,0]); 
                        else
                            img1 = draw_rectangle(img1,[x,y],[w+6,h+6],2,[0,153,0]); 
                        end
                    end
                    if state(5)>0
                        img1 = draw_rectangle(img1,[x,y],[w+8,h+8],2,[255,0,255]);
                    end
                    if state(6)>0
                        img1 = draw_rectangle(img1,[x,y],[w+10,h+10],2,[0,0,51]);            
                    end
                end          
                facenum(ii,2) = facenum(ii,2) + 1;
            end
            facenum(ii,1) = facenum(ii,1) + 1;
            facenum
            imwrite(img1,[savepath,file_list{i}{j},'.jpg']);
        end
    end
end
