FYSOS 2.0  aka   Konan   (C)opyright 1984-2018   Benjamin David Lunt

http://www.fysnet.net/fysos.htm
email:  fys [at] fysnet [dot] net

Dated: 09 Nov 2018

.Zip File contents:
  readme.txt      - this readme file
  a.img           - a 1.44meg bootable floppy image with the LeanFS File System
  fysos.img       - 10 Meg UEFI *and* Legacy BIOS bootable hard drive image
  qemu_efi.bat    - DOS batch file to start the QEMU emulation with EFI
  qemu_legacy.bat - DOS batch file to start the QEMU emulation with Legacy BIOS
  bochsrc.txt     - the resource file needed for Bochs
  OVMF.fd         - the EFI bios for QEMU

This is the readme file for instructions, directions, and notes about the
two images and the OS that is upon them.

  **** Please read all of this file before you send me an email since  *****
       there are a few things explained that will answer your first
       impression/questions.  :-)

This text file is best viewed in a fixed width font such as Courier New.

This is a bootable example of the Operating System I have been working on for
quite a few years, off and on of course, but still, I have enjoyed ever bit.

The a.img file is a LeanFS formatted, Legacy Bootable floppy image containing
the whole operating system.  No other files are necessary.

The fysos.img file is a EFI GPT formatted hard drive image with two
partitions.  The first is the bootable partition with the whole contents
of the operating system.  The second partition is an empty partition
just to show how to have another partition and that FYSOS can recognize it.

To boot and run the OS in QEMU:
 - to use an EFI boot, use the qemu_efi.bat batch file
    (please see the notes below)
 - to use a Legacy BIOS boot, use the qemu_legacy.bat batch file
    (please see the notes below)

To boot and run the OS in Oracle Virtual Box:
 - Set up VBox and point the system storage settings to both image files.
   - To boot UEFI, put a check in the EFI box under the system settings
     and set the boot sequence to boot the hard drive image.
    (Please note that only the hard drive image is EFI bootable)
   - To boot Legacy BIOS, remove the check in the EFI box.

To boot and run the OS in Bochs:
 - Set up Bochs to point to the included bochsrc.txt file.
   - You will need to modify the paths to the BIOS file, the VGA BIOS file,
     the image files, etc...
    (please see the notes below)


Notes:
 QEMU:
   1. The two batch files assume that the QEMU binary files are in the parent
      directory.  i.e.:  "..\qemu_32_executable_file.exe", etc.
   2. They also assume that the OVMF_VARS-pure-efi.fd and OVMF_CODE-pure-efi.fd
      files (the EFI bios), and the Legacy bios files are also in the parent directory.
   3. You must have a later version of QEMU since all version older than a
      few months ago had a bug that FYSOS failed upon.  The new version of
      QEMU does not have this bug and FYSOS no longer fails to read from the
      disk.
   4. You can get the latest version of QEMU for Windows at:
         https://qemu.weilnetz.de/  
       click on "32_bit", then scroll and get 
         qemu-w32-setup-20160903.exe
       (The good thing about this .exe installer is that it places all files
        in a single folder you specify.  No other file or folder is modified.
        If you ever update, simple choose the same folder and the next installer
        will overwrite any files necassary. To uninstall QEMU, simply delete
        that folder.  Period.  At least the Windows version anyway.)
 
 Oracle VBox:
   1. No batch files are included to start VBox.  If you know how to use VBox,
      you know how to set up the system to boot the files.
   2. VBox boots the EFI just fine.
   3. VBox boots the Legacy just fine.
   4. To get the latest version of VBox, go to:
        Oracle https://www.virtualbox.org/
   5. Please note that (at the moment) the fysos.img file does not have the
      required .VHD footer and VirtualBox may not load it because of this.
      Simply add the .VHD footer and it should work.  This is on my TODO list.

 Bochs:
   1. Of course Bochs does not have EFI capabilities, so no luck there.
      However, it boots the Legacy bios just fine.
   2. To get the latest version of Bochs, go to:
        Oracle http://bochs.sourceforge.net/
   3. Please note that I have a custom built version of Bochs and have not
      tried the downloaded version from that site.  If it doesn't boot my
      OS, please let me know.


General Notes:
  1. During boot up, as soon as you see "Loading FYSOS...", you may press the
     'F8' key (Function eight).  Once the loader is done loading the files, it
     will display a list of available screen modes.  Choose one using the alphabet
     letter associated with it (shown to the left).
     Not pressing 'F8' will default to a 1024x768x16-bit if available, falling
     back to a 1024x768x15-bit or a 800x600x16 bit.  If none of these are found,
     the list will be shown anyway.
  2. The text display and scrolling, both in the loader *and* the kernel are
     quite slow.  Okay, VERY slow.  The current form of text display uses a slow 
     technique displaying a single character at a time.  This was to get it to 
     work correctly.  My next step will be to display lines or groups of lines 
     at a time to make it much faster.
  3. Once the kernel has booted and you have a "DOS Prompt" style prompt, you
     may use it as it is very similar to DOS.
     *However*, please note that a recent change to the command line interface
     broke the way it handles paths.  Commands that require paths, such as 
     'copy' are picky on the paths for the source and destination and may
     corrupt the volume(s).  *Therefore* do not use on real hardware unless
     you don't care about the data on that volume.  A fix will be out as soon
     as I get to it...
  4. The GUI is included with this release.  At the prompt type "gui" and the
     enter key.  However, the GUI is just a demo since I used it for testing
     my code for Volume 6 of my book series.  It doesn't do much but window
     manipulation.  Also, if you exit out and then reload the GUI, it will
     fail.  My plans are not to exit the GUI once you have loaded it anyway.
     An exit from the GUI is a machine shutdown...
  5. I currently have the kernel stop just after it detects the Legacy ATA
     devices.  This is so I can work on items that need to be loaded from
     the media.  However, if you wish to let the kernel continue to load,
     type "exit" at the prompt and the kernel will continue to load other
     hardware drivers, including USB.  If you are familiar with your emulator's
     USB emulation, FYSOS will detect and use most devices.  For example, in 
     Bochs I could have the following line in my bochsrc.txt file:
       usb_uhci: enabled=1, port1=disk:usbdisk.img, options1=speed:full
     and Bochs will detect and mount the usbdisk.img file as a USB thumb drive.
     (Bochs automatically supports UHCI, no need to tell it to)
     Similarly, you can do the same for OHCI, EHCI, and xHCI, noting though
     that Bochs' EHCI emulation is not yet complete:
       pci: enabled=1, chipset=i440fx, slot1=cirrus, slot2=usb_xhci
       usb_ohci: enabled=1, port1=disk:usbdisk.img, options1=speed:full
     or
       pci: enabled=1, chipset=i440fx, slot1=cirrus, slot2=usb_ohci
       usb_ehci: enabled=1, port1=disk:usbdisk.img, options1=speed:full
     or
       pci: enabled=1, chipset=i440fx, slot1=cirrus, slot2=usb_ehci
       usb_xhci: enabled=1, port1=disk:usbdisk.img, options1=speed:full
     Note, that I have changed FYSOS considerably and have yet to make sure
     the USB still works :-).  Please let me know if it doesn't.....


I recommend that you only use this within emulators.  It is not ready for real
hardware due to the fact that it may corrupt file systems.  So, 

                ****** USE AT YOUR OWN RISK ******

If you have any comments, especially bug and/or error reports, please let me
know at the email address at the top of this file.

Thank you,
Ben

