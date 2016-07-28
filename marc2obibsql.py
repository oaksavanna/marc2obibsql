"""
The MIT License (MIT)

Copyright (c) 2016 Oak Savanna Library Services

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from datetime import datetime
from pymarc import MARCReader
from random import randint
import sys

if sys.argv[1]:
	file_name = sys.argv[1]
else:
	file_name = '/home/obib/default.mrc'

previous_tag = '000'
previous_subfield = '0'

with open(file_name, 'rb') as fh:
	out = open(file_name+'.sql', 'wb')
	reader = MARCReader(fh)
	for record in reader:
		bibid = str(randint(1, 10000))
		now = str(datetime.now());
		out.write('INSERT INTO biblio (bibid, create_dt, last_change_dt) VALUES (' + bibid + ", '" + now + "', '" + now + "');\n")
		for f in record.get_fields():
			if (previous_tag == f.tag):
				fieldseq = fieldseq + 1
			else:
				fieldseq = 1
			fieldid = str(randint(1, 1000000))
			if (f.is_control_field()):
				out.write('INSERT INTO biblio_field (bibid, fieldid, seq, tag, field_data) VALUES (' + bibid + ', ' + fieldid + ', ' + str(fieldseq) + ', '
					+ f.tag + ", '" + f.data + "');\n")
			else:
				out.write('INSERT INTO biblio_field (bibid, fieldid, seq, tag, ind1_cd, ind2_cd) VALUES (' + bibid + ', ' + fieldid + ', ' + str(fieldseq) + ', '
					+ f.tag + ", '" + f.indicators[0] + "', '" + f.indicators[1] + "');\n")
				for subfield in f:
					if (previous_subfield == subfield[0]):
						subfieldseq = subfieldseq + 1
					else:
						subfieldseq = 1
					subfieldid = str(randint(1, 10000000))
					out.write('INSERT INTO biblio_subfield (bibid, fieldid, subfieldid, seq, subfield_cd, subfield_data) VALUES (' + bibid + ', ' + fieldid + ', ' + subfieldid + ', '
						+ str(subfieldseq) + ", '"
						+ subfield[0] + "', '" + subfield[1].replace("'", "''") + "');\n")
			previous_tag = f.tag;

out.close()
