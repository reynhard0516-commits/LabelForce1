import Dexie from "dexie";
export const db = new Dexie("ImageLabelDB");
db.version(1).stores({
    labels: "++id, fileName, labels, timestamp"
});
