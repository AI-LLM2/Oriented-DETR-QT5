import xml.etree.ElementTree as ET
import os
import numpy as np
import matplotlib.pyplot as plt
import polyiou
from functools import partial
import argparse

def parse_gt(filename):
    """
    :param filename: ground truth file to parse
    :return: all instances in a picture
    """
    objects = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if line:
                splitlines = line.strip().split(' ')
                object_struct = {}
                if len(splitlines) < 9:
                    continue
                object_struct['name'] = splitlines[8]
                if len(splitlines) == 9:
                    object_struct['difficult'] = 0
                elif len(splitlines) == 10:
                    object_struct['difficult'] = int(splitlines[9])
                object_struct['bbox'] = [float(splitlines[0]),
                                         float(splitlines[1]),
                                         float(splitlines[2]),
                                         float(splitlines[3]),
                                         float(splitlines[4]),
                                         float(splitlines[5]),
                                         float(splitlines[6]),
                                         float(splitlines[7])]
                objects.append(object_struct)
            else:
                break
    return objects

def voc_ap(rec, prec, use_07_metric=False):
    """ ap = voc_ap(rec, prec, [use_07_metric])
    Compute VOC AP given precision and recall.
    If use_07_metric is true, uses the
    VOC 07 11 point method (default:False).
    """
    if use_07_metric:
        # 11 point metric
        ap = 0.
        for t in np.arange(0., 1.1, 0.1):
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(prec[rec >= t])
            ap = ap + p / 11.
    else:
        # correct AP calculation
        mrec = np.concatenate(([0.], rec, [1.]))
        mpre = np.concatenate(([0.], prec, [0.]))

        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        i = np.where(mrec[1:] != mrec[:-1])[0]
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap

def voc_eval(detpath, annopath, imagesetfile, classname, ovthresh=0.5, use_07_metric=False):
    """rec, prec, ap = voc_eval(detpath,
                                annopath,
                                imagesetfile,
                                classname,
                                [ovthresh],
                                [use_07_metric])
    Top level function that does the PASCAL VOC evaluation.
    """
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]

    recs = {}
    for i, imagename in enumerate(imagenames):
        recs[imagename] = parse_gt(annopath.format(imagename))

    class_recs = {}
    npos = 0
    for imagename in imagenames:
        R = [obj for obj in recs[imagename] if obj['name'] == classname]
        bbox = np.array([x['bbox'] for x in R])
        difficult = np.array([x['difficult'] for x in R]).astype(np.bool_)
        det = [False] * len(R)
        npos = npos + sum(~difficult)
        class_recs[imagename] = {'bbox': bbox, 'difficult': difficult, 'det': det}

    detfile = detpath.format(classname)
    with open(detfile, 'r') as f:
        lines = f.readlines()

    splitlines = [x.strip().split(' ') for x in lines]
    image_ids = [x[0] for x in splitlines]
    confidence = np.array([float(x[1]) for x in splitlines])

    BB = np.array([[float(z) for z in x[2:]] for x in splitlines])

    sorted_ind = np.argsort(-confidence)
    BB = BB[sorted_ind, :]
    image_ids = [image_ids[x] for x in sorted_ind]

    nd = len(image_ids)
    tp = np.zeros(nd)
    fp = np.zeros(nd)
    for d in range(nd):
        R = class_recs[image_ids[d]]
        bb = BB[d, :].astype(float)
        ovmax = -np.inf
        BBGT = R['bbox'].astype(float)

        if BBGT.size > 0:
            BBGT_xmin = np.min(BBGT[:, 0::2], axis=1)
            BBGT_ymin = np.min(BBGT[:, 1::2], axis=1)
            BBGT_xmax = np.max(BBGT[:, 0::2], axis=1)
            BBGT_ymax = np.max(BBGT[:, 1::2], axis=1)
            bb_xmin = np.min(bb[0::2])
            bb_ymin = np.min(bb[1::2])
            bb_xmax = np.max(bb[0::2])
            bb_ymax = np.max(bb[1::2])

            ixmin = np.maximum(BBGT_xmin, bb_xmin)
            iymin = np.maximum(BBGT_ymin, bb_ymin)
            ixmax = np.minimum(BBGT_xmax, bb_xmax)
            iymax = np.minimum(BBGT_ymax, bb_ymax)
            iw = np.maximum(ixmax - ixmin + 1., 0.)
            ih = np.maximum(iymax - iymin + 1., 0.)
            inters = iw * ih

            uni = ((bb_xmax - bb_xmin + 1.) * (bb_ymax - bb_ymin + 1.) +
                   (BBGT_xmax - BBGT_xmin + 1.) * (BBGT_ymax - BBGT_ymin + 1.) - inters)

            overlaps = inters / uni

            BBGT_keep_mask = overlaps > 0
            BBGT_keep = BBGT[BBGT_keep_mask, :]
            BBGT_keep_index = np.where(overlaps > 0)[0]

            def calcoverlaps(BBGT_keep, bb):
                overlaps = []
                for index, GT in enumerate(BBGT_keep):
                    overlap = polyiou.iou_poly(polyiou.VectorDouble(BBGT_keep[index]), polyiou.VectorDouble(bb))
                    overlaps.append(overlap)
                return overlaps

            if len(BBGT_keep) > 0:
                overlaps = calcoverlaps(BBGT_keep, bb)
                ovmax = np.max(overlaps)
                jmax = np.argmax(overlaps)
                jmax = BBGT_keep_index[jmax]

        if ovmax > ovthresh:
            if not R['difficult'][jmax]:
                if not R['det'][jmax]:
                    tp[d] = 1.
                    R['det'][jmax] = 1
                else:
                    fp[d] = 1.
        else:
            fp[d] = 1.

    fp = np.cumsum(fp)
    tp = np.cumsum(tp)
    rec = tp / float(npos)  # recall
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)  # precision
    ap = voc_ap(rec, prec, use_07_metric)

    return rec, prec, ap

def GetFileFromThisRootDir(dir, ext=None):
    allfiles = []
    needExtFilter = (ext is not None)
    for root, dirs, files in os.walk(dir):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles

def image2txt(srcpath, dstpath):
    filelist = GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        name = os.path.basename(os.path.splitext(fullname)[0])
        dstname = os.path.join(dstpath, 'imgnamefile.txt')
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
        with open(dstname, 'a') as f:
            f.writelines(name + '\n')

def parse_args():
    parser = argparse.ArgumentParser(description='MMDet test (and eval) a model')
    parser.add_argument('--detpath', default=r'E:\DETR\logs\swint_ohd\result_raw\Task1_{:s}.txt', help='test config file path')
    parser.add_argument('--annopath', default=r'E:\DETR\data\OHD-SJTU\after\test2017\labels\{:s}.txt', help='checkpoint file')
    parser.add_argument('--imagesetfile', default=r"E:\DETR\data\OHD-SJTU\after\test.txt", help='checkpoint file')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    detpath = args.detpath
    annopath = args.annopath
    imagesetfile = args.imagesetfile
    classnames = ['ship', 'plane']  # Example class names, modify as needed

    # Define IoU thresholds for AP50:95
    ovthreshes = np.arange(0.5, 1.0, 0.05)
    all_maps = []

    for classname in classnames:
        print('classname:', classname)
        class_maps = []
        for ovthresh in ovthreshes:
            rec, prec, ap = voc_eval(detpath, annopath, imagesetfile, classname, ovthresh=ovthresh, use_07_metric=True)
            class_maps.append(ap)
            print(f'AP@{ovthresh:.2f} for {classname}: {ap:.4f}')
        all_maps.append(class_maps)

    # Calculate AP50:95 for each class
    ap50_95_per_class = np.mean(all_maps, axis=1)
    for classname, ap50_95 in zip(classnames, ap50_95_per_class):
        print(f'mAP@50:95 for {classname}: {ap50_95:.4f}')

    # Calculate overall mAP@50:95
    overall_map50_95 = np.mean(ap50_95_per_class)
    print(f'Overall mAP@50:95: {overall_map50_95:.4f}')

if __name__ == '__main__':
    main()