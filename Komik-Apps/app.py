# melakukan proses import pymongo
import pymongo

# membuat config koneksi untuk menghubungkan mongodb dengan python
koneksi_url = "mongodb://localhost:27017"

# membuat sebuah function yang bertugas untuk mengecek koneksi ke mongodb
def cekMongoDB() :
    client = pymongo.MongoClient(koneksi_url)
    try:
        cek = client.list_database_names()
        print(cek)
    except:
        print("Database Tidak Terhubung")
# cekMongoDB()

# membuat sebuah function yang bertugas untuk create database
def createDatabase() :
    dbClient = pymongo.MongoClient(koneksi_url)
    namaDatabase = dbClient['Database_komik']
    namaCollection = namaDatabase['Komik']
    nilai_data = namaCollection.insert_one({ 'nama': "Detective Conan", 'pengarang': "Gosho Aoyama", 'harga' : 40000 })

    return nilai_data
# createDatabase()


class MongoCRUD:
    def __init__(self, data, koneksi):
        self.client = pymongo.MongoClient(koneksi)
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def bacaData(self):
        documents = self.collection.find()
        value = [{
            item: data[item] for item in data if item != '_id'} for data in documents]
        return value

    def buatData(self, data):
        new_documents = data['document']
        response = self.collection.insert_one(new_documents)
        value = {
            'Status' : 'Berhasil',
            'Document_id' : str(response.inserted_id)
        }
        return value

    def ubahData(self):
        data_awal = self.data['dataAwal']
        update_data = {
            "$set" : self.data['dataUbah']
        }

        response = self.collection.update_one(data_awal, update_data)
        value = {
            "Status" : "Berhasil Diupdate" if response.modified_count > 0 else "Data tidak Ditemukan"
        }

        print(value)
    
    def hapusData(self, data):
        dataHapus = data['document']
        response = self.collection.delete_one(dataHapus)
        value = {
            'Status' : 'Berhasil Dihapus' if response.deleted_count > 0 else "Data tidak Ditemukan"
        }

        print(value)


if __name__ == '__main__' :
    data = {
        "database" : "Database_komik",
        "collection" : "Komik",

        "dataAwal" : {
            "nama" : "Doraemon",
            "pengarang" : "Fujiko F. Fujio",
            "harga" : 55000
        },

        "dataUbah" : {
            "nama" : "Naruto",
            "pengarang" : "Masashi Kishimoto",
            "harga" : 48000
        }
    }

    data_hapus = {
        'document' : {
            "nama" : "Naruto",
            "pengarang" : "Masashi Kishimoto",
            "harga" : 48000
        }
    }

    

    # mongo_objek = MongoCRUD(data, koneksi_url)
    # baca_data = mongo_objek.bacaData()
    # print(baca_data)

    # mongo_objek = MongoCRUD(data, koneksi_url)
    # buat_data = mongo_objek.buatData({
    #         'document' : {
    #             "nama" : "Doraemon",
    #             "pengarang" : "Fujiko F. Fujio",
    #             "harga" : 55000
    #         }
    # })
    # print(buat_data)

    # mongo_objek = MongoCRUD(data, koneksi_url)
    # mongo_objek.ubahData()

    # mongo_objek = MongoCRUD(data, koneksi_url)
    # hapus = mongo_objek.hapusData(data_hapus)

