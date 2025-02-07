# read_jma_wp_v20210801.py
# Reading JMA Wind Profiler data in BUFR (edition 4) format
# Preliminary program: trying to read bits
# 2021-08-01 masudako

import numpy as np
from pathlib import Path

def int_from_bits(barray):
    nbit = len(barray)
    ival = 0
    for kbit in range(nbit):
        ival += barray[kbit] * 2**(nbit-kbit-1)
    return ival

##### Main program #####
def unfold(filename):
    
    with open(filename, 'rb') as f:
        bytes = f.read()

    f_out = open(filename.with_suffix(".csv"), "w")
    print("location,lat,lon,"
            "year,month,day,hour,minute,second,"
                "h_above_antenna,qc_info,u,v,w,snratio", file = f_out)

    # report header
    pos = 0
    print('### Report header')
    print(bytes[0:18])

    # BUFR section 0
    pos += 18
    print('### BUFR section 0')
    print(bytes[pos:pos+4])
    len_bufr_rec = bytes[pos+5-1]*256*256 + bytes[pos+6-1]*256 + bytes[pos+7-1]
    bufr_version = bytes[pos+8-1]+0
    print(len_bufr_rec, '# Length of BUFR record')
    print(bufr_version, '# BUFR version')

    # BUFR section 1
    pos += 8
    print('### BUFR section 1')
    len_sec_1 = bytes[pos+1-1]*256*256 + bytes[pos+2-1]*256 + bytes[pos+3-1]
    print(len_sec_1, '# Length of Section 1')
    revision = bytes[pos+9-1]
    print(revision, '# Revision')
    year   = bytes[pos+16-1]*256 + bytes[pos+17-1]
    month  = bytes[pos+18-1]
    day    = bytes[pos+19-1]
    hour   = bytes[pos+20-1]
    minute = bytes[pos+21-1]
    second = bytes[pos+22-1]
    print(year, month, day, hour, minute, second)

    # BUFR section 3
    pos += len_sec_1
    print('### BUFR section 3')
    len_sec_3 = bytes[pos+1-1]*256*256 + bytes[pos+2-1]*256 + bytes[pos+3-1]
    print(len_sec_3, '# Length of Section 3')
    n_subset = bytes[pos+5-1]*256 + bytes[pos+6-1]
    print(n_subset, '# n of subsets')

    # BUFR section 4
    pos += len_sec_3
    print('### BUFR section 4')
    len_sec_4 = bytes[pos+1-1]*256*256 + bytes[pos+2-1]*256 + bytes[pos+3-1]
    print(len_sec_4, '# Length of Section 4')
    sec4bytes = np.zeros(len_sec_4, dtype=np.uint8)
    for posbyte in range(len_sec_4 - 4):
        sec4bytes[posbyte] = bytes[pos + 4 + posbyte]
    sec4bits = np.unpackbits(sec4bytes)
    bitpos = 0
    for k_subset in range(n_subset):

        nbits  =  7
    ##  print(sec4bits[bitpos:bitpos+nbits])
        region = int_from_bits(sec4bits[bitpos:bitpos+nbits])
        print(region, '# region')
        bitpos += nbits

        nbits  = 10
    ##  print(sec4bits[bitpos:bitpos+nbits])
        stn_id = int_from_bits(sec4bits[bitpos:bitpos+nbits])
        print(stn_id, '# station id')
        bitpos += nbits

        nbits  = 15
    ##  print(sec4bits[bitpos:bitpos+nbits])
        lat = (int_from_bits(sec4bits[bitpos:bitpos+nbits]) -  9000) / 100.0
        print(lat, '# latitude')
        bitpos += nbits

        nbits  = 16
    ##  print(sec4bits[bitpos:bitpos+nbits])
        lon = (int_from_bits(sec4bits[bitpos:bitpos+nbits]) - 18000) / 100.0
        print(lon, '# longitude')
        bitpos += nbits

        nbits  = 15
    ##  print(sec4bits[bitpos:bitpos+nbits])
        height = int_from_bits(sec4bits[bitpos:bitpos+nbits]) - 400
        print(height, '# height')
        bitpos += nbits

        nbits  =  4
        instrument = int_from_bits(sec4bits[bitpos:bitpos+nbits])
        print(instrument, '# instrument')
        bitpos += nbits

        nbits  =  8
        n_rep_x = int_from_bits(sec4bits[bitpos:bitpos+nbits])
        print(n_rep_x, '# n of iteration x')
        bitpos += nbits

        for k_rep_x in range(n_rep_x):
    ##  for k_rep_x in [0]:

            nbits  = 12
            year = int_from_bits(sec4bits[bitpos:bitpos+nbits])
    ##      print(year, '# year')
            bitpos += nbits

            nbits  =  4
            month = int_from_bits(sec4bits[bitpos:bitpos+nbits])
    ##      print(month, '# month')
            bitpos += nbits

            nbits  =  6
            day = int_from_bits(sec4bits[bitpos:bitpos+nbits])
    ##      print(day, '# day')
            bitpos += nbits

            nbits  =  5
            hour = int_from_bits(sec4bits[bitpos:bitpos+nbits])
    ##      print(hour, '# hour')
            bitpos += nbits

            nbits  =  6
            minute = int_from_bits(sec4bits[bitpos:bitpos+nbits])
    ##      print(minute, '# minute')
            print(year, month, day, hour, minute)
            bitpos += nbits

            nbits  =  5
            time_spec = int_from_bits(sec4bits[bitpos:bitpos+nbits])
            print(time_spec, '# time_spec')
            bitpos += nbits

            nbits  = 12
            iv = int_from_bits(sec4bits[bitpos:bitpos+nbits])
            if (iv == 4095):
                duration = iv
            else:
                duration = iv - 2048
            print(duration, '# duration')
            bitpos += nbits

            nbits  =  8
            n_rep_y = int_from_bits(sec4bits[bitpos:bitpos+nbits])
            print(n_rep_y, '# n of iteration y')
            bitpos += nbits

            for k_rep_y in range(n_rep_y):
    ##      for k_rep_y in [0]:

                nbits  = 15
                h_above_antenna = int_from_bits(sec4bits[bitpos:bitpos+nbits])
    ##          print(h_above_antenna, '# height above antenna')
                bitpos += nbits

                nbits  =  8
                qc_info = int_from_bits(sec4bits[bitpos:bitpos+nbits])
    ##          print(qc_info, '# QC info')
                bitpos += nbits

                nbits  = 13
                iv = int_from_bits(sec4bits[bitpos:bitpos+nbits])
                if (iv == 8191):
                    u = iv
                else:
                    u = (iv - 4096) / 10.0
    ##          print(u, '# u')
                bitpos += nbits

                nbits  = 13
                iv = int_from_bits(sec4bits[bitpos:bitpos+nbits])
                if (iv == 8191):
                    v = iv
                else:
                    v = (iv - 4096) / 10.0
    ##          print(v, '# v')
                bitpos += nbits

                nbits  = 13
                iv = int_from_bits(sec4bits[bitpos:bitpos+nbits])
                if (iv == 8191):
                    w = iv
                else:
                    w = (iv - 4096) / 100.0
    ##          print(w, '# w')
                bitpos += nbits

                nbits  =  8
                iv = int_from_bits(sec4bits[bitpos:bitpos+nbits])
                if (iv == 255):
                    snratio = iv
                else:
                    snratio = iv - 32
    ##          print(snratio, '# S/N ratio')
    ##          データの取得する形を指定
                print(str(region)+str(stn_id), lat, lon, 
                    year, month, day, hour, minute, second,
                    h_above_antenna, qc_info, u, v, w, snratio,sep=",", file = f_out)
                # print(str(region)+str(stn_id), lat, lon, 
                #       "%04d-%02d-%02d %02d:%02d:%02d" % (year, month, day, hour, minute, second),
                #       h_above_antenna, qc_info, u, v, w, snratio,sep=",")
                bitpos += nbits

    # BUFR section 5
    pos += len_sec_4
    print('### BUFR section 5')
    print(bytes[pos+0:pos+4])

    f_out.close()

# パラメータ
year = 2020

for l in [str(year)+"_47406_47417_47423.send",str(year)+"_47585_47587_47590_47570.send",str(year)+"_47612_47640_47656.send",
          str(year)+"_47626_47629_47674.send",str(year)+"_47636_47663_47616.send",str(year)+"_47678_47795_47746.send",
          str(year)+"_47755_47893_47898.send",str(year)+"_47800_47805_47836_47912.send",str(year)+"_47819_47815_47822.send",
          str(year)+"_47848_47909_47945.send"]:

    directory = Path("D:\\master_research\\高層データ\\"+str(l))
    

    for file in directory.glob("**/*.send"):
        unfold(file)
