
import urllib.request
import json
import dml
import prov.model
import datetime
import uuid

class get(dml.Algorithm):
    contributor = 'houset_karamy'
    reads = []
    writes = ['houset_karamy.crimeReportsCambridge']

    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('houset_karamy', 'houset_karamy')
        
        dataSets = {'crimeReportsCambridge': 'https://data.cambridgema.gov/resource/dypy-nwuz.json'}  
        for ds in dataSets:
            url = dataSets[ds]
            response = urllib.request.urlopen(url).read().decode("utf-8")
            r = json.loads(response)
            s = json.dumps(r, sort_keys=True, indent=2)
            repo.dropPermanent(ds)
            repo.createPermanent(ds)
            repo['houset_karamy.' + ds].insert_many(r)
        
        repo.logout()
        
        endTime = datetime.datetime.now()
        
        return {"start":startTime, "end":endTime}
       
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('houset_karamy', 'houset_karamy')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        
      #writes = ['houset_karamy.crimeReportsCambridge','houset_karamy.crimeReportsBoston', 'houset_karamy.crimeReportsCambridge', 'houset_karamy.policeCarRoutesCambridge', 'houset_karamy.policeWalkingRoutesCambridge','houset_karamy.realTimeTravelMassdot']

            
        this_script = doc.agent('alg:houset_karamy#getCrimeReportsCambridge', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        resource1 = doc.entity('bdp:pyxn-r3i2', {'prov:label':'Police Stations', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
                        
        get_crimeReportsCambridge = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
#         get_hospitals = doc.activity('log:a'+str(uuid.uuid4()), startTime, endTime, {prov.model.PROV_TYPE:'ont:Retrieval', 'ont:Query':'?type=ad&?$select=ad,name'})

#         get_realTimeTravelMassDot = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(get_crimeReportsCambridge, this_script)

#         doc.wasAssociatedWith(get_realTimeTravelMassDot, this_script)
        
        doc.usage(get_crimeReportsCambridge, resource1, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'})
        

           
        crimeReportsCambridge = doc.entity('dat:houset_karamy#crimeReportsCambridge', {prov.model.PROV_LABEL:'Police Station Locations', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(crimeReportsCambridge, this_script)
        doc.wasGeneratedBy(crimeReportsCambridge, get_crimeReportsCambridge, endTime)
        doc.wasDerivedFrom(crimeReportsCambridge, resource1, get_crimeReportsCambridge, get_crimeReportsCambridge, get_crimeReportsCambridge) 
        

        repo.logout()
                  
        return doc


get.execute()
doc = get.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
