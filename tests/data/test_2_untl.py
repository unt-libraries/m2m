def processRecord(RecordClass, row):
   
    record = RecordClass('mphillips')

    record.mapping('basic', 'title', row['title'],
                    qualifier='officialtitle')

    record.mapping('agent', 'creator', row['author'],
                    qualifier='aut', agent_type='per', info='born somewhere')

    record.mapping('basic', 'date', row['date'],
                    qualifier='creation', required=False)

    record.setBaseDirectory('records')
    record.setFolderName(row['isbn'])
   
    return record
