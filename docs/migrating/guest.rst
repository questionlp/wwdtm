.. role:: bolditalic
   :class: bolditalic

*****
guest
*****

The following sections list out the changes that were made to the functions
migrated from ``libwwdtm`` to class methods under the ``wwdtm`` module
:py:mod:`wwdtm.guest`.

core → GuestAppearances
=======================

The following functions under the :py:mod:`wwdtm.guest.core` module have been
changed to become methods under :py:class:`wwdtm.guest.GuestAppearances`:

* :py:func:`retrieve_appearances_by_id`
* :py:func:`retrieve_appearances_by_slug`

details → Guest
===============

The following functions under the :py:mod:`wwdtm.guest.details` module have
been changed to become methods under :py:class:`wwdtm.guest.Guest`:

* :py:func:`retrieve_by_id`

  * Renamed to :py:meth:`retrieve_details_by_id`

* :py:func:`retrieve_by_slug`

  * Renamed to :py:meth:`retrieve_details_by_slug`

* :py:func:`retrieve_all`

  * Renamed to :py:meth:`retrieve_all_details`

info → Guest
============

The following functions under the :py:mod:`wwdtm.guest.info` module have been
changed to become methods under :py:class:`wwdtm.guest.Guest`:

* :py:func:`retrieve_all`
* :py:func:`retrieve_all_ids`
* :py:func:`retrieve_by_id`
* :py:func:`retrieve_by_slug`

utility → GuestUtility
======================

The following function under the :py:mod:`wwdtm.guest.utility` module have
been changed to become methods under :py:class:`wwdtm.guest.GuestUtility`:

* :py:func:`convert_id_to_slug`
* :py:func:`convert_slug_to_id`
* :py:func:`id_exists`
* :py:func:`slug_exists`

Deprecated Functions
====================

The following functions have been deprecated and were not migrated over from
the ``libwwdtm`` to ``wwdtm``:

* :py:func:`utility.validate_id`

  * Use :py:meth:`wwdtm.guest.GuestUtility.id_exists` instead

* :py:func:`utility.validate_slug`

  * Use :py:meth:`wwdtm.guest.GuestUtility.slug_exists` instead
