PROJECT_DIR="/home/burgercom/ihp.burgercom.co.za"
cd ${PROJECT_DIR}
rm -rf /tmp/ihp
cp -R backup_template/ /tmp/ihp
cp ihp/ihp.db /tmp/ihp/db
cp -R ihp/ /tmp/ihp/src
tar -zcvf /tmp/ihp-backup.tgz /tmp/ihp
rm -rf /tmp/ihp
mv /tmp/ihp-backup.tgz ihp/media


