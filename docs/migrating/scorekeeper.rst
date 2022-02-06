.. role:: bolditalic
   :class: bolditalic

***********
scorekeeper
***********

The following sections list out the changes that were made to the functions
migrated from ``libwwdtm`` to class methods under the ``wwdtm`` module
:py:mod:`wwdtm.scorekeeper`.

core → ScorekeeperAppearances
=============================

The following functions under the :py:mod:`wwdtm.scorekeeper.core` module have
been changed to become methods under
:py:class:`wwdtm.scorekeeper.ScorekeeperAppearances`:

* :py:func:`retrieve_appearances_by_id`
* :py:func:`retrieve_appearances_by_slug`

details → Scorekeeper
=====================

The following functions under the :py:mod:`wwdtm.scorekeeper.details` module
have been changed to become methods under
:py:class:`wwdtm.scorekeeper.Scorekeeper`:

* :py:func:`retrieve_by_id`

  * Renamed to :py:meth:`retrieve_details_by_id`

* :py:func:`retrieve_by_slug`

  * Renamed to :py:meth:`retrieve_details_by_slug`

* :py:func:`retrieve_all`

  * Renamed to :py:meth:`retrieve_all_details`

info → Scorekeeper
==================

The following functions under the :py:mod:`wwdtm.scorekeeper.info` module have
been changed to become methods under :py:class:`wwdtm.scorekeeper.Scorekeeper`:

* :py:func:`retrieve_all`
* :py:func:`retrieve_all_ids`
* :py:func:`retrieve_by_id`
* :py:func:`retrieve_by_slug`

utility → ScorekeeperUtility
============================

The following function under the :py:mod:`wwdtm.scorekeeper.utility` module
have been changed to become methods under
:py:class:`wwdtm.scorekeeper.ScorekeeperUtility`:

* :py:func:`convert_id_to_slug`
* :py:func:`convert_slug_to_id`
* :py:func:`id_exists`
* :py:func:`slug_exists`

Deprecated Functions
====================

The following functions have been deprecated and were not migrated over from
``libwwdtm`` to ``wwdtm``:

* :py:func:`utility.validate_id`

  * Use :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.id_exists` instead

* :py:func:`utility.validate_slug`

  * Use :py:meth:`wwdtm.scorekeeper.ScorekeeperUtility.slug_exists` instead
