import cv2
import argparse
import sys

import source.compare_fcn as compare


def compute(img1=None, img2=None, action=None, args=None):
    if args:
        img1 = args.img1
        img2 = args.img2
        action = args.action

    cv_img1 = cv2.imread(img1)
    cv_img2 = cv2.imread(img2)

    print('action is {}'.format(action))
    if action == 'difference_threshold':
        returned = compare.difference_threshold(cv_img1, cv_img2)
    elif action == 'difference_box':
        returned = compare.compare_box(cv_img1, cv_img2)
    elif action == 'difference_sk':
        returned = compare.difference_sk(cv_img1, cv_img2)
    else:
        return None

    return returned


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-1", '--img1', type=str, required=True)
    parser.add_argument("-2", '--img2', type=str, required=True)
    parser.add_argument("-s", '--save', type=bool, required=False)
    parser.add_argument("-d", '--display', type=bool, required=False)
    parser.add_argument("-a", '--action', type=str, required=True)
    args = parser.parse_args()

    returned = compute(args=args)

    if len(returned) == 0:
        print('function didnt return anything')
        sys.exit(1)

    if args.save:
        for index, file in enumerate(returned):
            # print(args.action + '_' + compare.image_title[file])
            cv2.imwrite(args.action + '_' + compare.image_title[index] + '.jpg', file)

    if args.display:
        for index, file in enumerate(returned):
            cv2.imshow(args.action + '_' + compare.image_title[index], file)

        cv2.waitKey(0)
        # closing all open windows
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
