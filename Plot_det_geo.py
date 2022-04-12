import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm, colors, patches

def get_specs():
    ######################
    # Setup the geometry #
    ######################
    geo = container()
    geo.det_type = 'Eiger2 CdTe' # [str] Pilatus3 / Eiger2
    geo.det_size = '4M'          # [str]  300K 1M 2M 6M / 1M 4M 9M 16M
    geo.dist = 8.0               # [cm]   Detector distance
    geo.tilt = 25.0              # [deg]  Detector tilt
    geo.rota = 0.0               # [deg]  detector rotation
    geo.yoff = 6.0               # [cm]   Detector offset (vertical)
    geo.energy = 21.0            # [keV]  Beam energy
    geo.unit = 'd'               # [tdqs] Contour legend (t: 2-Theta, d: d-spacing, q: q-space, s: sin(theta)/lambda)
    geo.origin = True            # [bool] plot contour lines for original geometry?

    ###########################
    # Detector Specifications #
    ###########################
    det = container()
    if geo.det_type.startswith('Pilatus'):
        ###############################
        # Specifications for Pilatus3 #
        ###############################
        det.hms = 8.38    # [cm]  module size (horizontal)
        det.vms = 3.35    # [cm]  module size (vertical)
        det.pxs = 172e-4  # [cm]  pixel size
        det.hgp = 7       # [pix] gap between modules (horizontal)
        det.vgp = 17      # [pix] gap between modules (vertical)
        det.name = f'{geo.det_type} {geo.det_size}'
        det.sizes = {'300K':(1,3),'1M':(2,5),'2M':(3,8),'6M':(5,12)}
        if geo.det_size not in det.sizes.keys():
            print('Unknown detector type/size combination!')
            raise SystemExit
        det.hmn, det.vmn = det.sizes[geo.det_size]
    elif geo.det_type.startswith('Eiger'):
        #############################
        # Specifications for Eiger2 #
        #############################
        det.hms = 7.71    # [cm]  module size (horizontal)
        det.vms = 3.84    # [cm]  module size (vertical)
        det.pxs = 75e-4   # [cm]  pixel size
        det.hgp = 38      # [pix] gap between modules (horizontal)
        det.vgp = 12      # [pix] gap between modules (vertical)
        det.name = f'{geo.det_type} {geo.det_size}'
        det.sizes = {'1M':(1,2),'4M':(2,4),'9M':(3,6),'16M':(4,8)}
        if geo.det_size not in det.sizes.keys():
            print('Unknown detector type/size combination!')
            raise SystemExit
        det.hmn, det.vmn = det.sizes[geo.det_size]
    else:
        ###########################################
        # ADD CUSTOM DETECTOR SPECIFICATIONS HERE #
        ###########################################
        det.hms = 10.0    # [cm]  module size (horizontal)
        det.vms = 14.0    # [cm]  module size (vertical)
        det.pxs = 10e-4   # [cm]  pixel size
        det.hgp = 0       # [pix] gap between modules (horizontal)
        det.vgp = 0       # [pix] gap between modules (vertical)
        det.hmn = 1       # [int] number of modules (horizontal)
        det.vmn = 1       # [int] number of modules (vertical)
        det.name = f'{geo.det_type} {geo.det_size}'

    ################
    # Plot Details #
    ################
    plo = container()
    plo.cont_levels = np.logspace(-1,1,num=25)/2  # contour levels
    plo.cont_fsize = 8                            # contour label size
    plo.cont_geom_alpha = 1.00                    # contour alpha (geometry)
    plo.cont_geom_cmap = cm.get_cmap('viridis_r') # contour colormap (geometry)
    plo.cont_orig_alpha = 0.10                    # contour alpha (original)
    plo.cont_orig_color = 'black'                 # contour color (original)
    plo.cont_reso = 500                           # contour steps (accuracy)
    plo.cont_xmax = 50                            # max x/y for drawing contours
    plo.module_alpha = 0.20                       # detector module alpha
    plo.module_color = 'black'                    # detector module color
    plo.margin_top = 0.93                         # plot margin for title
    plo.plot_size = 7                             # plot size
    plo.debug_3d = False                          # [bool] DEBUG plot 3D cones?

    ###################################
    # !!! Don't change below here !!! #
    ###################################
    return geo, det, plo

def main():
    # fetch the geometry, detector and plot specifications
    geo, det, plo = get_specs()
    # translate unit for plot title
    unit_names = {'t':'2-Theta',
                  'd':'d-spacing',
                  'q':'q-space',
                  's':'sin(Theta)/lambda'}
    if geo.unit not in unit_names.keys():
        print('Unknown contour label unit!')
        raise SystemExit
    # figure out proper plot dimensions
    plo.xdim = (det.hms * det.hmn + det.pxs * det.hgp * det.hmn)
    plo.ydim = (det.vms * det.vmn + det.pxs * det.vgp * det.vmn)
    plo.fig_ratio = plo.xdim / plo.ydim
    # init the plot
    fig = plt.figure(figsize=(plo.plot_size * plo.margin_top * plo.fig_ratio, plo.plot_size))
    ax = fig.add_subplot(111)
    # limit the axes
    ax.set_xlim(-plo.xdim/2, plo.xdim/2)
    ax.set_ylim(-plo.ydim/2, plo.ydim/2)
    # setup detector and geometry
    build_detector(ax, det, plo)
    # create cones and draw contour lines
    draw_contours(ax, geo, plo)
    # add title / information
    plt.suptitle(f'{det.name} | Energy: {geo.energy} keV | Distance: {geo.dist} cm\nRotation: {geo.rota}° | Tilt: {geo.tilt}° | Offset: {geo.yoff} cm | Units: {unit_names[geo.unit]}', size=10)
    # adjust the margins
    plt.subplots_adjust(top=plo.margin_top, bottom=0, right=1, left=0, hspace=0, wspace=0)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.show()
    # plot the 3d cones?
    if plo.debug_3d:
        plot_3d(geo, plo)

def build_detector(ax, det, plo):
    # build detector modules
    # beam position is between the modules (even) or at the center module (odd)
    # determined by the "+det.hmn%2" part
    for i in range(-det.hmn//2+det.hmn%2, det.hmn-det.hmn//2):
        for j in range(-det.vmn//2+det.vmn%2, det.vmn-det.vmn//2):
            # place modules along x (i) and y (j) keeping the gaps in mind ( + (det.hgp*det.pxs)/2)
            # the " - ((det.hms+det.hgp*det.pxs)/2)" positions the origin (the beam) at the center of a module
            # and "det.hmn%2" makes sure this is only active for detectors with an odd number of modules
            origin_x = i*(det.hms+det.hgp*det.pxs) - ((det.hms+det.hgp*det.pxs)/2)*(det.hmn%2) + (det.hgp*det.pxs)/2
            origin_y = j*(det.vms+det.vgp*det.pxs) - ((det.vms+det.vgp*det.pxs)/2)*(det.vmn%2) + (det.vgp*det.pxs)/2
            ax.add_patch(patches.Rectangle((origin_x, origin_y),  det.hms, det.vms, color=plo.module_color, alpha=plo.module_alpha))

def draw_contours(ax, geo, plo):
    # draw contour lines
    for n,i in enumerate(plo.cont_levels):
        # calculate resolution rings
        # 2-Theta: np.arctan(dist/(dist/i))
        thr = np.arctan(1/i)/2
        # Conversion factor keV to Angstrom: 12.398
        # sin(t)/l: np.sin(Theta) / lambda -> (12.398/geo_energy)
        stl = np.sin(thr)/(12.398/geo.energy)
        # d-spacing: l = 2 d sin(t) -> 1/2(sin(t)/l)
        dsp = 1/(2*stl)
        # figure out the labels
        unit_dict = {'n':None, 't':np.rad2deg(2*thr),
                     'd':dsp, 'q':stl*4*np.pi, 's':stl}
        # draw contours for the original geometry
        if geo.origin:
            X,Y,Z = create_cone(i, 0, 0, 0, geo.dist, plo.cont_xmax, plo.cont_reso)
            # don't draw contour lines that are out of bounds
            # make sure Z is large enough to draw the contour
            if np.max(Z) >= geo.dist:
                c0 = ax.contour(X, Y, Z, [geo.dist], colors=plo.cont_orig_color, alpha=plo.cont_orig_alpha)
                # label original geometry contours
                fmt = {c0.levels[0]:f'{np.round(unit_dict[geo.unit],2):.2f}'}
                ax.clabel(c0, c0.levels, inline=True, fontsize=plo.cont_fsize, fmt=fmt, manual=[(plo.xdim,plo.ydim)])
        # draw contours for the tilted/rotated/moved geometry
        X,Y,Z = create_cone(i, geo.rota, geo.tilt, geo.yoff, geo.dist, plo.cont_xmax, plo.cont_reso)
        # make sure Z is large enough to draw the contour
        if np.max(Z) >= geo.dist:
            c1 = ax.contour(X, Y, Z, [geo.dist], colors=colors.to_hex(plo.cont_geom_cmap((n+1)/len(plo.cont_levels))), alpha=plo.cont_geom_alpha)
            # label moved geometry contours
            fmt = {c1.levels[0]:f'{np.round(unit_dict[geo.unit],2):.2f}'}
            ax.clabel(c1, c1.levels, inline=True, fontsize=plo.cont_fsize, fmt=fmt, manual=[(0,plo.ydim)])

def create_cone(dim, rota, tilt, yoff, geo_dist, plt_cont_xmax, plt_cont_reso):
    # creating grid
    x = np.linspace(-plt_cont_xmax,plt_cont_xmax,plt_cont_reso)
    X,Y = np.meshgrid(x,x)
    # set z values
    Z = np.sqrt(X**2+Y**2)*dim
    # rotate the sample around y
    a = np.deg2rad(tilt) + np.deg2rad(rota)
    t = np.transpose(np.array([X,Y,Z]), (1,2,0))
    m = [[np.cos(a), 0, np.sin(a)],[0,1,0],[-np.sin(a), 0, np.cos(a)]]
    X,Y,Z = np.transpose(np.dot(t, m), (2,0,1))
    # compensate for tilt
    comp = np.deg2rad(tilt) * geo_dist
    return Y,X+comp-yoff,Z

def plot_3d(geo, plo):
    #####################################################
    # - debug - debug - debug - debug - debug - debug - #
    # - to check geometry, offset, tilt and rotation  - #
    #####################################################
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #plt_cont_levels = [0.01, 0.10, 0.20, 0.30, 0.39, 0.42, 0.45, 0.49, 0.53, 0.58, 0.65, 0.75, 0.87, 1.00, 1.16, 1.50, 2.00, 3.00, 5.00, 10.00]
    for n,i in enumerate(plo.cont_levels[-3:]):
        #ax.plot_surface(*create_cone(i, geo_tilt, geo_yoff), alpha=0.25)
        ax.plot_wireframe(*create_cone(i, 0, 0, 0, geo.dist, plo.cont_xmax, plo.cont_reso), alpha=0.1, colors='gray')
        ax.contour(*create_cone(i, 0, 0, 0, geo.dist, plo.cont_xmax, plo.cont_reso), [geo.dist], alpha=0.1, colors='gray')

        ax.plot_wireframe(*create_cone(i, geo.rota, geo.tilt, geo.yoff, geo.dist, plo.cont_xmax, plo.cont_reso), alpha=0.25, colors='red')
        ax.contour(*create_cone(i, geo.rota, geo.tilt, geo.yoff, geo.dist, plo.cont_xmax, plo.cont_reso), [geo.dist], colors='red')

    ax.set_xlim(-plo.cont_xmax/2, plo.cont_xmax/2)
    ax.set_ylim(-plo.cont_xmax/2, plo.cont_xmax/2)
    ax.set_zlim(0, geo.dist)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

class container(object):
    pass

if __name__ == '__main__':
    main()
