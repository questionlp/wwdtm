.. role:: bolditalic
   :class: bolditalic

****
show
****

The following sections list out the changes that were made to the functions
migrated from ``libwwdtm`` to class methods under the ``wwdtm`` module
:py:mod:`wwdtm.show`.

core → ShowInfo
===============

The following functions under the :py:mod:`wwdtm.show.core` module have been
changed to become methods under :py:class:`wwdtm.show.ShowInfo`:

* :py:func:`retrieve_bluff_info_by_id`
* :py:func:`retrieve_core_info_by_id`
* :py:func:`retrieve_guest_info_by_id`
* :py:func:`retrieve_panelist_info_by_id`

details → Show
==============

The following functions under the :py:mod:`wwdtm.show.details` module have
been changed to become methods under :py:class:`wwdtm.show.Show`:

* :py:func:`retrieve_by_id`

  * Renamed to :py:meth:`retrieve_details_by_id`

* :py:func:`retrieve_all`

  * Renamed to :py:meth:`retrieve_all_details`

* :py:func:`retrieve_by_date`

  * Renamed to :py:meth:`retrieve_details_by_date`

* :py:func:`retrieve_by_date_string`

  * Renamed to :py:meth:`retrieve_details_by_date_string`

* :py:func:`retrieve_by_year`

  * Renamed to :py:meth:`retrieve_details_by_year`

* :py:func:`retrieve_by_year_month`

  * Renamed to :py:meth:`retrieve_details_by_year_month`

* :py:func:`retrieve_recent`

  * Renamed to :py:meth:`retrieve_recent_details`

info → Show
===========

The following functions under the :py:mod:`wwdtm.show.info` module have been
changed to become methods under :py:class:`wwdtm.show.Show`:

* :py:func:`retrieve_all`
* :py:func:`retrieve_all_dates`
* :py:func:`retrieve_all_dates_tuple`
* :py:func:`retrieve_all_ids`
* :py:func:`retrieve_all_scores_by_year`
* :py:func:`retrieve_all_show_years_months`
* :py:func:`retrieve_all_show_years_months_tuple`
* :py:func:`retrieve_by_date`
* :py:func:`retrieve_by_date_string`
* :py:func:`retrieve_by_id`
* :py:func:`retrieve_by_year`
* :py:func:`retrieve_by_year_month`
* :py:func:`retrieve_months_by_year`
* :py:func:`retrieve_recent`
* :py:func:`retrieve_years`

utility → ShowUtility
=====================

The following function under the :py:mod:`wwdtm.show.utility` module have
been changed to become methods under :py:class:`wwdtm.show.ShowUtility`:

* :py:func:`convert_date_to_id`
* :py:func:`convert_id_to_date`
* :py:func:`id_exists`
* :py:func:`date_exists`

Deprecated Functions
====================

The following functions have been deprecated and were not migrated over from
the ``libwwdtm`` to ``wwdtm``:

* :py:func:`utility.validate_id`

  * Use :py:meth:`wwdtm.show.showUtility.id_exists` instead
