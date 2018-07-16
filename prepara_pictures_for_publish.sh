
srcfolder=collected
dstfolder="ready-to-publish"
processedfolder=processed

echo Entring source folder: $srcfolder
cd $srcfolder

echo Processing the images
find . -type f -iname "*.jpg_large" -print0 | while IFS= read -r -d $'\0' line; do
    filebasename=$(basename $line)
    filenamenoextension="${filebasename%.*}"
    dstfilename=../$dstfolder/$filenamenoextension.png
    echo "$line. Base name is $filebasemane and destination is $dstfilename"
    convert $line $dstfilename
    echo "Moving file to processed folder ../$processedfolder"
    mv $line ../$processedfolder
    echo "Done"
done

echo

# Convert the files to png format
#mogrify -format png /home/sergio/Documents/bible_wallpapers/collected/*.jpg_large

# Move the processed files to correct destination
#mv /home/sergio/Documents/bible_wallpapers/collected/*.jpg_large /home/sergio/Documents/bible_wallpapers/processed/
#mv /home/sergio/Documents/bible_wallpapers/collected/*.png /home/sergio/Documents/bible_wallpapers/ready-yo-publish/


