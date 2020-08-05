if [[ $DESKTOP_SESSION == regolith ]]; then
                de=Regolith

            elif [[ $XDG_CURRENT_DESKTOP ]]; then
                # If $XDG_CURRENT_DESKTOP is not "Unity" (this is an old value used by canonical Unity)
                # Actually return a DE, as the value is with 90% certainty used to workaround some appindicator issues with the users WM
                if [[ $XDG_CURRENT_DESKTOP != "Unity" ]]; then
                    de=${XDG_CURRENT_DESKTOP/X\-}
                    de=${de/Budgie:GNOME/Budgie}
                    de=${de/:Unity7:ubuntu}
                fi

            elif [[ $DESKTOP_SESSION ]]; then
                de=${DESKTOP_SESSION##*/}

            elif [[ $GNOME_DESKTOP_SESSION_ID ]]; then
                de=GNOME

            elif [[ $MATE_DESKTOP_SESSION_ID ]]; then
                de=MATE

            elif [[ $TDE_FULL_SESSION ]]; then
                de=Trinity

            fi
type -p xprop &>/dev/null && {
            id=$(xprop -root -notype _NET_SUPPORTING_WM_CHECK)
            id=${id##* }
            wm=$(xprop -id "$id" -notype -len 100 -f _NET_WM_NAME 8t)
            wm=${wm/*WM_NAME = }
            wm=${wm/\"}
            wm=${wm/\"*}
        }
            if [ ! -z $de ];then
                echo $de
            fi
                echo $wm
