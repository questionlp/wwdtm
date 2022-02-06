.. role:: bolditalic
   :class: bolditalic

********
location
********

The following sections list out the changes that were made to the functions
migrated from ``libwwdtm`` to class methods under the ``wwdtm`` module
:py:mod:`wwdtm.location`.

core → LocationRecordings
=========================

The following functions under the :py:mod:`wwdtm.location.core` module have been
changed to become methods under :py:class:`wwdtm.location.LocationRecordings`:

* :py:func:`retrieve_recordings_by_id`
* :bolditalic:`(New):` :py:func:`retrieve_recordings_by_slug`

  * This was missing in ``libwwdtm`` but has been implemented in ``wwdtm``

details → LocationRecordings
============================

The following functions under the :py:mod:`wwdtm.location.details` module have
been changed to become methods under
:py:class:`wwdtm.location.LocationRecordings`:

* :py:func:`retrieve_recordings_by_id`

  * Renamed to :py:meth:`retrieve_details_by_id`

* :py:func:`retrieve_recordings_by_slug`

  * Renamed to :py:meth:`retrieve_details_by_slug`

details → Location
==================

The following functions under the :py:mod:`wwdtm.location.details` module have
been changed to become methods under :py:class:`wwdtm.location.Location`:

* :py:func:`retrieve_all_recordings`

  * Renamed to :py:meth:`retrieve_all_details`

info → location
===============

The following functions under the :py:mod:`wwdtm.location.info` module have been
changed to become methods under :py:class:`wwdtm.location.Location`:

* :py:func:`retrieve_all`
* :py:func:`retrieve_all_ids`
* :py:func:`retrieve_by_id`
* :py:func:`retrieve_by_slug`

utility → locationUtility
=========================

The following function under the :py:mod:`wwdtm.location.utility` module have
been changed to become methods under :py:class:`wwdtm.location.LocationUtility`:

* :py:func:`convert_id_to_slug`
* :py:func:`convert_slug_to_id`
* :py:func:`id_exists`
* :py:func:`slug_exists`

Deprecated Functions
====================

The following functions have been deprecated and were not migrated over from
the ``libwwdtm`` to ``wwdtm``:

* :py:func:`utility.validate_id`

  * Use :py:meth:`wwdtm.location.locationUtility.id_exists` instead

* :py:func:`utility.validate_slug`

  * Use :py:meth:`wwdtm.location.locationUtility.slug_exists` instead
