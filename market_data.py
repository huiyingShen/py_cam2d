

def getMarketDataRaw():
    labels =    """
                edy: 72.0,97.0 196.0,75.0
                trk: 72.0,146.0 460.0,81.0
                gld: 71.0,194.0 386.0,142.0
                mcl: 71.0,244.0 337.0,199.0
                grv: 73.0,338.0 211.0,314.0
                drt: 72.0,364.0 81.0,363.0
                hys: 71.0,389.0 162.0,370.0
                fel: 72.0,437.0 95.0,434.0
                plk: 72.0,298.0 91.0,421.0 104.0,431.0
                lrk: 104.0,77.0 152.0,381.0
                hyd: 171.0,75.0 210.0,312.0
                lvn: 240.0,75.0 263.0,209.0
                jns: 309.0,75.0 331.0,206.0
                tyl: 377.0,75.0 388.0,135.0
                jse: 165.0,457.0 195.0,426.0
                msn: 214.0,458.0 488.0,182.0
                hwr: 342.0,458.0 487.0,308.0
                fls: 465.0,456.0 488.0,435.0
                10: 130.0,459.0 113.0,440.0
                9th: 229.0,459.0 159.0,390.0
                8th: 352.0,460.0 221.0,327.0
                7th: 490.0,412.0 287.0,212.0
                6th: 490.0,231.0 400.0,147.0
                rsc: 442.0,457.0 393.0,409.0
                lng: 489.0,457.0 416.0,383.0
                mrk: 79.0,460.0 393.0,149.0 400.0,144.0 471.0,74.0
                mrk: 89.0,458.0 397.0,152.0 401.0,137.0 426.0,117.0
                dgp: 132.0,160.0 128.0,137.0
                cta: 226.0,192.0 220.0,169.0
                prm: 137.0,281.0 156.0,277.0 167.0,270.0 179.0,269.0 190.0,271.0 204.0,270.0 192.0,271.0 182.0,279.0 168.0,280.0 155.0,277.0
                sfl: 262.0,276.0 263.0,286.0 269.0,289.0 276.0,283.0 275.0,277.0 269.0,275.0 263.0,278.0
                lsk: 214.0,397.0 244.0,427.0
                rus: 489.0,324.0 442.0,277.0
                """
    legends =   """
                10: 10th street -- northwest to southeast
                6TH: 6th street -- northwest to southeast
                7TH: 7th street -- northwest to southeast
                8TH: 8th street -- northwest to southeast
                9TH: 9th street -- northwest to southeast
                DRT: Dr. Tom Waddell Place -- east to west
                EDY: Eddy street -- east to west
                FEL: Fell street -- east to west
                FLS: Folsom street -- Northeast to southwest
                GLD: Golden Gate Avenue -- east to west
                GRV: Grove street -- east to west
                HWR: Howard street -- Northeast to southwest
                HYD: Hyde street -- north to south
                HYS: Hayes street -- east to west
                JNS: Jones street -- north to south
                LNG: Langton street -- northwest to southeast
                LRK: Larkin street -- north to south
                LVN: Leavenworth street -- north to south
                MRK: Market street -- Northeast to southwest
                MS1: Mason street -- north to south
                MSN: Mission street -- Northeast to southwest
                PLK: Polk street -- north to south
                TRK: Turk street -- east to west
                TYL: Taylor street -- north to south
                JSE: Jessie Street -- Northeast to southwest
                DGP: dodge place -- north to south
                CTA: continuum alley -- north to south
                PRM: pioneer monument
                SFL: san francisco lighthouse for the blind and visually impaired
                LSK: Laskie Street -- northwest to southeast
                RUS: russ street -- northwest to southeast
                RSC: Rausch street -- northwest to southeast
                MCL: Mcallister street -- east to west
                """
    return labels,legends

def split_strip(sIn):
    out = []
    for s in sIn.split('\n'):
        s = s.strip()
        if len(s) < 3: continue
        try:
            s2 = s.split(':')
            # print(s2)
            out.append([s2[0].upper(),s2[1]])
        except:
            print("error", s)
    return out

def getMarketData():
    labels,legends = getMarketDataRaw()
    streets = split_strip(labels)
    for i in range(len(streets)):
        vPt = streets[i][1].split(' ')
        pLine = []
        for pt in vPt:
            try:
                xy = pt.split(',')
                pLine.append((float(xy[0]),float(xy[1])))
            except:
                pass; #print(xy)
        streets[i][1] = pLine
    legends = split_strip(legends)
    nm_des = {}
    for nm,des in legends:
        nm_des[nm] = des
    return streets,nm_des


if __name__ == "__main__":
    lbl,lgd = getMarketData()
    # print(lgd)
    
