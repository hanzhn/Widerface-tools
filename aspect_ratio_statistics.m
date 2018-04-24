clear
set = {'train';'val'}

th1 = 512*sqrt(2)
th2 = 1024*sqrt(2)
facenum = zeros(2,2);% to save the num of faces
ar_histogram=zeros(2,200);
for ii=1:size(set)
load(strcat('/home/smiles/hz/databases/WIDER-face/annotation_2017/wider_face_',set{ii},'.mat'));
    for i=1:size(event_list)        
        for j=1:size(file_list{i})
            n=0;
            for k=1:size(face_bbx_list{i}{j})
                x = face_bbx_list{i}{j}(k,1);
                y = face_bbx_list{i}{j}(k,2);
                w = face_bbx_list{i}{j}(k,3);
                h = face_bbx_list{i}{j}(k,4);
                if ~w || ~h
                    continue;
                end
                if w>th2|| h>th2 || w<th1 || h<th1
                    continue
                end
                ar = floor(double(w)/double(h)*100);
                ar = max(ar,1); 
                if ar>200
                    ar=200;
                end
                ar_histogram(ii,ar) = ar_histogram(ii,ar) + 1;
                n = n+1;
                facenum(ii,2) = facenum(ii,2) + 1;
            end
            facenum(ii,1) = facenum(ii,1) + 1;
        end
     end
end
facenum

figure(1)
plot(1:1:200,ar_histogram(1,:))
figure(2)
plot(1:1:200,ar_histogram(2,:))