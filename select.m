%% Generates the train and validation picture list for training.
%   Change the exclude_invalid_faces and other conditions to filter the
%   annotation.

clear
set = {'train','val'}
exclude_invalid_faces = 0
hard_event ={'14','21','0-','2-','17','10','35','23','47','46','8-','18','16','22','3-','6-','7-','24','38','56'}

face_num = zeros(2,2);% to save the num of faces
skip_pic_num = 0;
for ii=1:size(set,2)
    load(strcat('/home/smiles/hz/databases/WIDER-face/annotation_2017/wider_face_',set{ii},'.mat'));
    pic_list_file = fopen(strcat('data/WIDER_',set{ii},'_easy&medium_60.txt'), 'w+');
    for i=1:size(event_list)
        
        isHard = 0;
        for index = 1:size(hard_event,2)
            event = hard_event{index};
            if event(1) == event_list{i}(1) && event(2) == event_list{i}(2)
                isHard = 1;
                break;
            end
        end
        if isHard
            continue;
        end
            
        for j=1:size(file_list{i})
            %get the widths and heights, write the pic names and pic paths to picpath txt
            jpg_name = strcat('/home/smiles/hz/databases/WIDER-face/WIDER_',set{ii},'/images/',event_list{i},'/',file_list{i}{j},'.jpg');
            n = 0;
            for k=1:size(face_bbx_list{i}{j}) 
%                 if exclude_invalid_faces && invalid_label_list{i}{j}(k)>=1  % Change here
%                     continue;
%                 end
                n = n +1;
            end
            if n<60
                fprintf( pic_list_file, strcat(file_list{i}{j},'\n') );
                face_num(ii,1) = face_num(ii,1) + 1;
                face_num(ii,2) = face_num(ii,2) + n;
            else
                skip_pic_num = skip_pic_num + 1;
                fprintf('skip\n')
            end
        end
    end
    fclose(pic_list_file);
end
face_num
skip_pic_num