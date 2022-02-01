.. role:: bolditalic
   :class: bolditalic

********
panelist
********

The following sections list out the changes that were made to the functions
migrated from ``libwwdtm`` to class methods under the ``wwdtm`` module
:py:mod:`wwdtm.panelist`.

core → PanelistAppearances
==========================

The following functions under the :py:mod:`wwdtm.panelist.core` module have
been changed to become methods under
:py:class:`wwdtm.panelist.PanelistAppearances`:

* :py:func:`retrieve_appearances_by_id`
* :py:func:`retrieve_appearances_by_slug`

core → PanelistScores
=====================

The following functions under the :py:mod:`wwdtm.panelist.core` module have
been changed to become methods under :py:class:`wwdtm.panelist.PanelistScores`:

* :py:func:`retrieve_scores_by_id`
* :bolditalic:`(New):` :py:meth:`retrieve_scores_by_slug`

  * This was missing in ``libwwdtm`` but has been implemented in ``wwdtm``

core → PanelistStatistics
=========================

The following functions under the :py:mod:`wwdtm.panelist.core` module have
been changed to become methods under
:py:class:`wwdtm.panelist.PanelistStatistics`:

* :py:func:`retrieve_bluffs_by_id`
* :py:func:`retrieve_bluffs_by_slug`
* :py:func:`retrieve_rank_info_by_id`
* :bolditalic:`(New):` :py:func:`retrieve_rank_info_by_slug`

  * This was missing in ``libwwdtm`` but has been implemented in ``wwdtm``

* :py:func:`retrieve_statistics_by_id`
* :py:func:`retrieve_statistics_by_slug`

details → Panelist
==================

The following functions under the :py:mod:`wwdtm.panelist.details` module
have been changed to become methods under :py:class:`wwdtm.panelist.Panelist`:

* :py:func:`retrieve_by_id`

  * Renamed to :py:meth:`retrieve_details_by_id`

* :py:func:`retrieve_by_slug`

  * Renamed to :py:meth:`retrieve_details_by_slug`

* :py:func:`retrieve_all`

  * Renamed to :py:meth:`retrieve_all_details`

info → Panelist
===============

The following functions under the :py:mod:`wwdtm.panelist.info` module have
been changed to become methods under :py:class:`wwdtm.panelist.Panelist`:

* :py:func:`retrieve_all`
* :py:func:`retrieve_all_ids`
* :py:func:`retrieve_by_id`
* :py:func:`retrieve_by_slug`

info → PanelistAppearances
==========================

The following functions under the :py:mod:`wwdtm.panelist.info` module have
been changed to become methods under
:py:class:`wwdtm.panelist.PanelistAppearances`:

* :py:func:`retrieve_yearly_appearances_by_id`
* :py:func:`retrieve_yearly_appearances_by_slug`

info → PanelistScores
---------------------

The following functions under the :py:mod:`wwdtm.panelist.info` module have
been changed to become methods under :py:class:`wwdtm.panelist.PanelistScores`:

* :py:func:`retrieve_scores_grouped_list_by_id`
* :py:func:`retrieve_scores_grouped_list_by_slug`
* :py:func:`retrieve_scores_grouped_ordered_pair_by_id`
* :py:func:`retrieve_scores_grouped_ordered_pair_by_slug`
* :py:func:`retrieve_scores_list_by_id`
* :py:func:`retrieve_scores_list_by_slug`
* :py:func:`retrieve_scores_ordered_pair_by_id`
* :py:func:`retrieve_scores_ordered_pair_by_slug`

utility → PanelistUtility
-------------------------

The following function under the :py:mod:`wwdtm.panelist.utility` module have
been changed to become methods under :py:class:`wwdtm.panelist.PanelistUtility`:

* :py:func:`convert_id_to_slug`
* :py:func:`convert_slug_to_id`
* :py:func:`id_exists`
* :py:func:`slug_exists`

Deprecated Functions
--------------------

The following functions have been deprecated and were not migrated over from
the ``libwwdtm`` to ``wwdtm``:

* :py:func:`utility.validate_id`

  * Use :py:meth:`wwdtm.panelist.PanelistUtility.id_exists` instead

* :py:func:`utility.validate_slug`

  * Use :py:meth:`wwdtm.panelist.PanelistUtility.slug_exists` instead
