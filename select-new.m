clear
set = {'train';'val'}

facenum = zeros(2,2);% to save the num of faces
skip = 0;
for ii=1:size(set)
load(strcat('/home/smiles/hz/databases/WIDER-face/annotation/wider_face_',set{ii},'.mat'));
piclistfile = fopen(strcat('data/WIDER_within30faces_',set{ii},'.txt'), 'w+');

for i=1:size(event_list)        
    for j=1:size(file_list{i})
        %get the widths and heights, write the pic names and pic paths to picpath txt
        jpgname = strcat('/home/smiles/hz/databases/WIDER-face/WIDER_',set{ii},'/images/',event_list{i},'/',file_list{i}{j},'.jpg');
        n = 0;
        for k=1:size(face_bbx_list{i}{j})
            if invalid_label_list{i}{j}(k)>=1 || occlusion_label_list{i}{j}(k)>=2
                continue;
            end
        n = n +1;
        end
        if n>=1 && n<=30
            fprintf( piclistfile, strcat(jpgname,'\n') );
            facenum(ii,1) = facenum(ii,1) + 1;
            facenum(ii,2) = facenum(ii,2) + n;
        else
            skip = skip + 1;
            fprintf('skip\n')
        end
    end
end

fclose(piclistfile);
end
facenum
skip